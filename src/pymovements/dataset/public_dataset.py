# Copyright (c) 2023 The pymovements Project Authors
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
"""This module provides the abstract base public dataset class."""
from __future__ import annotations

from abc import ABCMeta
from pathlib import Path
from urllib.error import URLError

from pymovements.dataset.dataset import Dataset
from pymovements.dataset.dataset_definition import DatasetDefinition
from pymovements.dataset.dataset_library import DatasetLibrary
from pymovements.utils.archives import extract_archive
from pymovements.utils.downloads import download_file


class PublicDataset(Dataset, metaclass=ABCMeta):
    """Extends the :py:class:`~pymovements.Dataset` base class with functionality for downloading
    and extracting public datasets.

    To implement this abstract base class for a new dataset, the attributes/properties `_mirrors`
    and `_resources` must be implemented.
    """

    def __init__(
            self,
            definition: str | DatasetDefinition | type[DatasetDefinition],
            *,
            root: str | Path,
            dataset_dirname: str | None = None,
            downloads_dirname: str = 'downloads',
            raw_dirname: str = 'raw',
            preprocessed_dirname: str = 'preprocessed',
            events_dirname: str = 'events',
    ):
        """Initialize the public dataset object.

        You can set up a custom directory structure by populating the particular dirname attributes.
        See :py:attr:`~pymovements.dataset.PublicDataset.dataset_dirname`,
        :py:attr:`~pymovements.dataset.PublicDataset.raw_dirname`,
        :py:attr:`~pymovements.dataset.PublicDataset.preprocessed_dirname` and
        :py:attr:`~pymovements.dataset.PublicDataset.events_dirname` and
        :py:attr:`~pymovements.dataset.PublicDataset.downloads_dirname` for details.

        Parameters
        ----------
        root : str, Path
            Path to the root directory of the dataset.
        dataset_dirname : str, optional
            Dataset directory name under root path. Can be `.` if dataset is located in root path.
            Default: `.`
        downloads_dirname : str, optional
            Name of directory to store downloaded data.Default: `downloads`
        raw_dirname ; str, optional
            Name of directory under dataset path that contains raw data. Can be `.` if raw data is
            located in dataset path. We advise the user to keep the original raw data separate from
            the preprocessed / event data. Default: `raw`
        preprocessed_dirname : str, optional
            Name of directory under dataset path that will be used to store preprocessed data. We
            advise the user to keep the preprocessed data separate from the original raw data.
            Default: `preprocessed`
        events_dirname : str, optional
            Name of directory under dataset path that will be used to store event data. We advise
            the user to keep the event data separate from the original raw data. Default: `events`
        """
        if isinstance(definition, str):
            definition = DatasetLibrary.get(definition)()

        if isinstance(definition, type):
            definition = definition()

        if dataset_dirname is None:
            dataset_dirname = definition.name

        super().__init__(
            root=root,
            experiment=definition.experiment,
            filename_regex=definition.filename_regex,
            filename_regex_dtypes=definition.filename_regex_dtypes,
            custom_read_kwargs=definition.custom_read_kwargs,
            dataset_dirname=dataset_dirname,
            raw_dirname=raw_dirname,
            preprocessed_dirname=preprocessed_dirname,
            events_dirname=events_dirname,
        )
        self.mirrors = definition.mirrors
        self.resources = definition.resources
        self.downloads_dirname = downloads_dirname

    def download(self, *, extract: bool = True, remove_finished: bool = False) -> Dataset:
        """Download dataset.

        This downloads all resources of the dataset. Per default this also extracts all archives
        into :py:meth:`Dataset.raw_rootpath`,
        To save space on your device you can remove the archive files after
        successful extraction with ``remove_finished=True``.

        If a corresponding file already exists in the local system, its checksum is calculated and
        checked against the expected checksum.
        Downloading will be evaded if the integrity of the existing file can be verified.
        If the existing file does not match the expected checksum it is overwritten with the
        downloaded new file.

        Parameters
        ----------
        extract : bool
            Extract dataset archive files.
        remove_finished : bool
            Remove archive files after extraction.

        Raises
        ------
        AttributeError
            If number of mirrors or number of resources specified for dataset is zero.
        RuntimeError
            If downloading a resource failed for all given mirrors.

        Returns
        -------
        PublicDataset
            Returns self, useful for method cascading.
        """
        if len(self.mirrors) == 0:
            raise AttributeError('number of mirrors must not be zero to download dataset')

        if len(self.resources) == 0:
            raise AttributeError('number of resources must not be zero to download dataset')

        self.raw_rootpath.mkdir(parents=True, exist_ok=True)

        for resource in self.resources:
            success = False

            for mirror in self.mirrors:

                url = f'{mirror}{resource["resource"]}'

                try:
                    download_file(
                        url=url,
                        dirpath=self.downloads_rootpath,
                        filename=resource['filename'],
                        md5=resource['md5'],
                    )
                    success = True

                # pylint: disable=overlapping-except
                except (URLError, OSError, RuntimeError) as error:
                    print(f'Failed to download (trying next):\n{error}')
                    # downloading the resource, try next mirror
                    continue

                # downloading the resource was successful, we don't need to try another mirror
                break

            if not success:
                raise RuntimeError(
                    f"downloading resource {resource['resource']} failed for all mirrors.",
                )

        if extract:
            self.extract(remove_finished=remove_finished)

        return self

    def extract(self, remove_finished: bool = False) -> Dataset:
        """Extract dataset archives.

        Parameters
        ----------
        remove_finished : bool
            Remove archive files after extraction.

        Returns
        -------
        PublicDataset
            Returns self, useful for method cascading.
        """
        self.raw_rootpath.mkdir(parents=True, exist_ok=True)

        for resource in self.resources:
            extract_archive(
                source_path=self.downloads_rootpath / resource['filename'],
                destination_path=self.raw_rootpath,
                recursive=True,
                remove_finished=remove_finished,
            )
        return self

    @property
    def path(self) -> Path:
        """The path to the dataset directory.

        The dataset path points to the dataset directory under the root path. Per default the
        dataset directory name is equal to the class name.

        Example
        -------
        Let's define a custom class first with one mirror and one resource.
        >>> class CustomPublicDataset(DatasetDefinition):
        ...     mirrors = ['https://www.example.com/']
        ...     resources = [
        ...         {
        ...             'resource': 'relative_path_to_resource',
        ...             'filename': 'example_dataset.zip',
        ...             'md5': 'md5md5md5md5md5md5md5md5md5md5md',
        ...         },
        ...     ]

        The default behaviour is to locate the data set in a directory under the root path with the
        same name as the class name:
        >>> dataset = PublicDataset(CustomPublicDataset, root='/path/to/all/your/datasets')
        >>> dataset.path  # doctest: +SKIP
        Path('/path/to/all/your/datasets/CustomPublicDataset')

        You can specify an explicit dataset directory name:
        >>> dataset = PublicDataset(
        ...     CustomPublicDataset,
        ...     root='/path/to/all/your/datasets',
        ...     dataset_dirname='custom_dataset',
        ... )
        >>> dataset.path  # doctest: +SKIP
        Path('/path/to/all/your/datasets/custom_dataset')

        You can specify to use the root path to be the actual dataset directory:
        >>> dataset = PublicDataset(
        ...     CustomPublicDataset,
        ...     root='/path/to/your/dataset/',
        ...     dataset_dirname='.',
        ... )
        >>> dataset.path  # doctest: +SKIP
        Path('/path/to/your/dataset')
        """
        return super().path

    @property
    def downloads_rootpath(self) -> Path:
        """The path to the directory of the raw data.

        The download path points to the download directory under the root path.

        Example
        -------
        Let's define a custom class first with one mirror and one resource.
        >>> class CustomPublicDataset(DatasetDefinition):
        ...     mirrors: tuple[str] = ('https://www.example.com/', )
        ...     resources: tuple[dict[str, str]] = (
        ...         {
        ...             'resource': 'relative_path_to_resource',
        ...             'filename': 'example_dataset.zip',
        ...             'md5': 'md5md5md5md5md5md5md5md5md5md5md',
        ...         },
        ...     )

        >>> dataset = PublicDataset(CustomPublicDataset, root='/path/to/your/datasets/')
        >>> dataset.downloads_rootpath  # doctest: +SKIP
        Path('/path/to/your/datasets/CustomPublicDataset/downloads')

        You can also explicitely specify the preprocessed directory name. The default is `raw`.
        >>> dataset = PublicDataset(
        ...     CustomPublicDataset,
        ...     root='/path/to/your/datasets/',
        ...     dataset_dirname='your_dataset',
        ...     downloads_dirname='your_raw_data',
        ... )
        >>> dataset.downloads_rootpath  # doctest: +SKIP
        Path('/path/to/your/datasets/your_dataset/your_raw_data')

        If your raw data is not in a separate directory under the root path then you can also
        specify `.` as the directory name. We discourage this and advise the user to keep raw data
        and preprocessed data separated.
        ... dataset = Dataset(
        >>> dataset = PublicDataset(
        ...     CustomPublicDataset,
        ...     root='/path/to/your/datasets/',
        ...     dataset_dirname='your_dataset',
        ...     raw_dirname='.',
        ... )
        >>> dataset.preprocessed_rootpath  # doctest: +SKIP
        Path('/path/to/your/datasets/your_dataset/your_raw_data')
        """
        return self.path / self.downloads_dirname