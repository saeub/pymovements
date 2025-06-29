# Copyright (c) 2023-2025 The pymovements Project Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""DatasetDefinition module."""
from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from warnings import warn

import yaml

from pymovements._utils._html import repr_html
from pymovements.dataset._utils._resources import _HasResourcesIndexer
from pymovements.dataset._utils._yaml import reverse_substitute_types
from pymovements.dataset._utils._yaml import substitute_types
from pymovements.dataset._utils._yaml import type_constructor
from pymovements.gaze.experiment import Experiment


yaml.add_multi_constructor('!', type_constructor, Loader=yaml.SafeLoader)


@repr_html()
@dataclass
class DatasetDefinition:
    """Definition to initialize a :py:class:`~pymovements.dataset.Dataset`.

    Attributes
    ----------
    name: str
        The name of the dataset. (default: '.')
    long_name: str | None
        The entire name of the dataset. (default: None)
    has_files: dict[str, bool]
        Indicate whether the dataset contains 'gaze', 'precomputed_events', and
        'precomputed_reading_measures'.
    mirrors: dict[str, list[str]] | dict[str, tuple[str, ...]]
        A list of mirrors of the dataset. Each entry must be of type `str` and end with a '/'.
        (default: field(default_factory=dict))
    resources: dict[str, list[dict[str, str]]] | dict[str, tuple[dict[str, str], ...]]
        A list of dataset resources. Each list entry must be a dictionary with the following keys:
        - `resource`: The url suffix of the resource. This will be concatenated with the mirror.
        - `filename`: The filename under which the file is saved as.
        - `md5`: The MD5 checksum of the respective file.
        (default: field(default_factory=dict))
    experiment: Experiment | None
        The experiment definition. (default: None)
    extract: dict[str, bool] | None
        Decide whether to extract the data. (default: None)
        .. deprecated:: v0.22.1
        This field will be removed in v0.27.0.
    filename_format: dict[str, str]
        Regular expression which will be matched before trying to load the file. Namedgroups will
        appear in the `fileinfo` dataframe. (default: field(default_factory=dict))
    filename_format_schema_overrides: dict[str, dict[str, type]]
        If named groups are present in the `filename_format`, this makes it possible to cast
        specific named groups to a particular datatype. (default: field(default_factory=dict))
    custom_read_kwargs: dict[str, dict[str, Any]]
        If specified, these keyword arguments will be passed to the file reading function. The
        behavior of this argument depends on the file extension of the dataset files.
        If the file extension is `.csv` the keyword arguments will be passed
        to :py:func:`polars.read_csv`. If the file extension is`.asc` the keyword arguments
        will be passed to :py:func:`pymovements.utils.parsing.parse_eyelink`.
        See Notes for more details on how to use this argument.
        (default: field(default_factory=dict))
    column_map : dict[str, str]
        The keys are the columns to read, the values are the names to which they should be renamed.
        (default: field(default_factory=dict))
    trial_columns: list[str] | None
            The name of the trial columns in the input data frame. If the list is empty or None,
            the input data frame is assumed to contain only one trial. If the list is not empty,
            the input data frame is assumed to contain multiple trials and the transformation
            methods will be applied to each trial separately. (default: None)
    time_column: str | None
        The name of the timestamp column in the input data frame. This column will be renamed to
        ``time``. (default: None)

    time_unit: str | None
        The unit of the timestamps in the timestamp column in the input data frame. Supported
        units are 's' for seconds, 'ms' for milliseconds and 'step' for steps. If the unit is
        'step' the experiment definition must be specified. All timestamps will be converted to
        milliseconds. (default: 'ms')

    pixel_columns: list[str] | None
        The name of the pixel position columns in the input data frame. These columns will be
        nested into the column ``pixel``. If the list is empty or None, the nested ``pixel``
        column will not be created. (default: None)
    position_columns: list[str] | None
        The name of the dva position columns in the input data frame. These columns will be
        nested into the column ``position``. If the list is empty or None, the nested
        ``position`` column will not be created. (default: None)
    velocity_columns: list[str] | None
        The name of the velocity columns in the input data frame. These columns will be nested
        into the column ``velocity``. If the list is empty or None, the nested ``velocity``
        column will not be created. (default: None)
    acceleration_columns: list[str] | None
        The name of the acceleration columns in the input data frame. These columns will be
        nested into the column ``acceleration``. If the list is empty or None, the nested
        ``acceleration`` column will not be created. (default: None)
    distance_column : str | None
        The name of the column containing eye-to-screen distance in millimeters for each sample
        in the input data frame. If specified, the column will be used for pixel to dva
        transformations. If not specified, the constant eye-to-screen distance will be taken from
        the experiment definition. This column will be renamed to ``distance``. (default: None)

    Notes
    -----
    When working with the ``gaze_custom_read_kwargs`` attribute there are specific use cases and
    considerations to keep in mind, especially for reading csv files:

    1. Custom separator
    To read a csv file with a custom separator, you can pass the `separator` keyword argument to
    ``gaze_custom_read_kwargs``. For example pass ``gaze_custom_read_kwargs={'separator': ';'}`` to
    read a semicolon-separated csv file.

    2. Reading subset of columns
    To read only specific columns, specify them in ``gaze_custom_read_kwargs``. For example:
    ``gaze_custom_read_kwargs={'columns': ['col1', 'col2']}``

    3. Specifying column datatypes
    ``polars.read_csv`` infers data types from a fixed number of rows, which might not be accurate
    for the entire dataset. To ensure correct data types, you can pass a dictionary to the
    ``schema_overrides`` keyword argument in ``gaze_custom_read_kwargs``.
    Use data types from the `polars` library.
    For instance:
    ``gaze_custom_read_kwargs={'schema_overrides': {'col1': polars.Int64, 'col2': polars.Float64}}``
    """

    # pylint: disable=too-many-instance-attributes

    name: str = '.'

    long_name: str | None = None

    has_files: dict[str, bool] = field(default_factory=dict)

    mirrors: dict[str, list[str]] | dict[str, tuple[str, ...]] = field(default_factory=dict)

    resources: dict[str, list[dict[str, str]]] | dict[str, tuple[dict[str, str], ...]] = field(
        default_factory=dict,
    )

    experiment: Experiment | None = field(default_factory=Experiment)

    extract: dict[str, bool] | None = None

    filename_format: dict[str, str] = field(default_factory=dict)

    filename_format_schema_overrides: dict[str, dict[str, type]] = field(default_factory=dict)

    custom_read_kwargs: dict[str, dict[str, Any]] = field(default_factory=dict)

    column_map: dict[str, str] = field(default_factory=dict)

    trial_columns: list[str] | None = None
    time_column: str | None = None
    time_unit: str | None = None
    pixel_columns: list[str] | None = None
    position_columns: list[str] | None = None
    velocity_columns: list[str] | None = None
    acceleration_columns: list[str] | None = None
    distance_column: str | None = None

    _has_resources: _HasResourcesIndexer = field(
        default_factory=_HasResourcesIndexer, init=False, repr=False, compare=False, hash=False,
    )

    @staticmethod
    def from_yaml(path: str | Path) -> DatasetDefinition:
        """Load a dataset definition from a YAML file.

        Parameters
        ----------
        path: str | Path
            Path to the YAML definition file

        Returns
        -------
        DatasetDefinition
            Initialized dataset definition
        """
        with open(path, encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # Convert experiment dict to Experiment object if present
        if 'experiment' in data:
            data['experiment'] = Experiment.from_dict(data['experiment'])

        data = reverse_substitute_types(data)
        # Initialize DatasetDefinition with YAML data
        return DatasetDefinition(**data)

    def to_dict(
        self,
        *,
        exclude_private: bool = True,
        exclude_none: bool = True,
    ) -> dict[str, Any]:
        """Return dictionary representation.

        Parameters
        ----------
        exclude_private: bool
            Exclude attributes that start with ``_``.
        exclude_none: bool
            Exclude attributes that are either ``None`` or that are objects that evaluate to
            ``False`` (e.g., ``[]``, ``{}``, ``EyeTracker()``). Attributes of type ``bool``,
            ``int``, and ``float`` are not excluded.

        Returns
        -------
        dict[str, Any]
            Dictionary representation of dataset definition.
        """
        data = asdict(self)

        # Delete private fields from dictionary.
        if exclude_private:
            for key in list(data.keys()):
                if key.startswith('_'):
                    del data[key]

        # Delete fields that evaluate to False (False, None, [], {})
        if exclude_none:
            for key, value in list(data.items()):
                if not isinstance(value, (bool, int, float)) and not value:
                    del data[key]

        if 'experiment' in data and data['experiment'] is not None:
            data['experiment'] = data['experiment'].to_dict(exclude_none=exclude_none)
        return data

    def to_yaml(
        self,
        path: str | Path,
        *,
        exclude_private: bool = True,
        exclude_none: bool = True,
    ) -> None:
        """Save a dataset definition to a YAML file.

        Parameters
        ----------
        path: str | Path
            Path where to save the YAML file to.
        exclude_private: bool
            Exclude attributes that start with ``_``.
        exclude_none: bool
            Exclude attributes that are either ``None`` or that are objects that evaluate to
            ``False`` (e.g., ``[]``, ``{}``, ``EyeTracker()``). Attributes of type ``bool``,
            ``int``, and ``float`` are not excluded.
        """
        data = self.to_dict(exclude_private=exclude_private, exclude_none=exclude_none)

        data = substitute_types(data)

        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, sort_keys=False)

    @property
    def has_resources(self) -> _HasResourcesIndexer:
        """Checks for resources in :py:attr:`~pymovements.dataset.DatasetDefinition.resources`.

        This read-only property checks if there are any resources set in
        :py:attr:`~pymovements.dataset.DatasetDefinition.resources`. It can be used as a `bool` or
        as an indexable class. In a boolean context it checks if there are any resources set in the
        :py:cls:`~pymovements.dataset.DatasetDefinition`. Furthermore, you can index the property
        to check if there are any resources set for a given content type.

        Examples
        --------
        This custom :py:cls:`~pymovements.dataset.DatasetDefinition` has no resources defined:
        >>> import pymovements as pm
        >>> my_definition = pm.DatasetDefinition('MyDatasetWithoutOnlineResources', resources=None)
        >>> my_definition.has_resources
        False

        A :py:cls:`~pymovements.dataset.DatasetDefinition` from our
        :py:cls:`~pymovements.dataset.DatasetLibrary` will usually have some online resources
        defined:
        >>> definition = pm.DatasetLibrary.get('ToyDataset')
        >>> definition.has_resources
        True

        You can also check if a specific content type is contained in the resources:
        >>> definition.has_resources['gaze']
        True

        In this definition there are gaze resources defined, but no precomputed events.
        >>> definition.has_resources['precomputed_events']
        False
        """
        # Resources may have changed, so update indexer before returning.
        # A better way to update the resources would be through a resources setter property.
        self._has_resources.set_resources(self.resources)
        return self._has_resources

    def __post_init__(self) -> None:
        """Handle special attributes."""
        if self.extract is not None:
            warn(
                DeprecationWarning(
                    'DatasetDefinition.extract is deprecated since version v0.22.1. '
                    'This field will be removed in v0.27.0.',
                ),
            )
