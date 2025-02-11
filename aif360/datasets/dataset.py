# importing ABC, this module provides infrastructure for defining abstract base classes
# these compliment duck typing (programming style doesnt look at object;s type to detemine if it has right interface
# ABCs do this by providing way to define interfaces when other techniques (e.g. hasattr()) would be clumsy/wrong
# ABCs introduce virtual subclasses, classe which don't inherit from a class but are still recognised by isinstance() and issubclass()
# can create own ABCs with abc module
from abc import ABC, abstractmethod

# used for shallow and deep copy operations
import copy

# defining Dataset class, inheriting ABC class
class Dataset(ABC):
    """Abstract base class for datasets."""

    @abstractmethod                                                             #decorator
    def __init__(self, **kwargs):                                               #constructor
        self.metadata = kwargs.pop('metadata', dict()) or dict()
        self.metadata.update({
            'transformer': '{}.__init__'.format(type(self).__name__),
            'params': kwargs,
            'previous': []
        })
        self.validate_dataset()

    def validate_dataset(self):
        """Error checking and type validation."""
        pass

    def copy(self, deepcopy=False):
        """Convenience method to return a copy of this dataset.

        Args:
            deepcopy (bool, optional): :func:`~copy.deepcopy` this dataset if
                `True`, shallow copy otherwise.

        Returns:
            Dataset: A new dataset with fields copied from this object and
            metadata set accordingly.
        """
        cpy = copy.deepcopy(self) if deepcopy else copy.copy(self)
        # preserve any user-created fields
        cpy.metadata = cpy.metadata.copy()
        cpy.metadata.update({
            'transformer': '{}.copy'.format(type(self).__name__),
            'params': {'deepcopy': deepcopy},
            'previous': [self]
        })
        return cpy

    @abstractmethod
    def export_dataset(self):
        """Save this Dataset to disk."""
        raise NotImplementedError

    @abstractmethod
    def split(self, num_or_size_splits, shuffle=False):
        """Split this dataset into multiple partitions.

        Args:
            num_or_size_splits (array or int): If `num_or_size_splits` is an
                int, *k*, the value is the number of equal-sized folds to make
                (if *k* does not evenly divide the dataset these folds are
                approximately equal-sized). If `num_or_size_splits` is an array
                of type int, the values are taken as the indices at which to
                split the dataset. If the values are floats (< 1.), they are
                considered to be fractional proportions of the dataset at which
                to split.
            shuffle (bool, optional): Randomly shuffle the dataset before
                splitting.

        Returns:
            list(Dataset): Splits. Contains *k* or `len(num_or_size_splits) + 1`
            datasets depending on `num_or_size_splits`.
        """
        raise NotImplementedError
