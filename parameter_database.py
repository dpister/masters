from __future__ import annotations
from dataclasses import dataclass
import sqlite3
from types import TracebackType
from typing import Type

from spin import SpinRing

from math_helper import indices_mapping

from config import config


@dataclass
class NpyDataPaths:
    """"""

    x_values_path: str
    eigenvalues_path: str
    eigenvectors_path: str

    @staticmethod
    def from_parameter_id(parameter_id: int) -> NpyDataPaths:
        x_values_path: str = config["data_paths"]["npy_files"]["x_values"]
        eigenvalues_path: str = config["data_paths"]["npy_files"]["x_values"]
        eigenvectors_path: str = config["data_paths"]["npy_files"]["x_values"]
        return NpyDataPaths(
            x_values_path=x_values_path.format(parameter_id),
            eigenvalues_path=eigenvalues_path.format(parameter_id),
            eigenvectors_path=eigenvectors_path.format(parameter_id),
        )


class Database:
    """"""

    def __init__(self, database_path: str):
        self._database_path = database_path

    def __enter__(self) -> Database:
        self._connection = sqlite3.connect(self._database_path)
        self._cursor = self._connection.cursor()
        return self

    def __exit__(
        self,
        type: Type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        self._connection.close()


class ParameterDatabase(Database):
    """"""

    _CREATE_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS parameters (
            parameter_id INTEGER PRIMARY KEY,
            B_x REAL,
            B_y REAL,
            B_z REAL,
            B_type TEXT NOT NULL CHECK (B_type IN ('circular', 'linear')),
            D REAL,
            J REAL,
            s REAL,
            N INTEGER,
            D_angle REAL,
            x_values_npy_path TEXT,
            eigenvalues_npy_path TEXT,
            eigenvectors_npy_path TEXT
        )
        """

    _GET_PARAMETER_ID_QUERY = """
        SELECT parameter_id
        FROM parameters 
        WHERE
        B_x = ? AND
        B_y = ? AND
        B_z = ? AND
        B_type = ? AND
        D = ? AND
        J = ? AND
        s = ? AND
        N = ? AND
        D_angle = ?
        """

    _INSERT_PARAMETERS_QUERY = """
        INSERT INTO parameters (
            B_x,
            B_y,
            B_z,
            B_type,
            D,
            J,
            s,
            N,
            D_angle,
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

    _UPDATE_DATA_PATHS_QUERY = """
        UPDATE parameters 
        SET 
            x_values_npy_path = ? 
            eigenvalues_npy_path = ?
            eigenvectors_npy_path = ?
        WHERE parameter_id = ?
        """

    _GET_DATAPATHS_QUERY = """
        SELECT  (
            x_values_npy_path, 
            eigenvalues_npy_path,
            eigenvectors_npy_path
        )
        FROM parameters 
        WHERE parameter_id = ?
        """

    def __enter__(self) -> ParameterDatabase:
        super().__enter__()
        self._cursor.execute(self._CREATE_TABLE_QUERY)
        self._connection.commit()
        return self

    def get_parameter_id(self, spin_ring: SpinRing) -> int | None:
        row = self._cursor.execute(
            self._GET_PARAMETER_ID_QUERY,
            (
                spin_ring.magnetic_field_of_first_spin[indices_mapping["x"]],
                spin_ring.magnetic_field_of_first_spin[indices_mapping["y"]],
                spin_ring.magnetic_field_of_first_spin[indices_mapping["z"]],
                spin_ring.magnetic_field_type,
                spin_ring.heisenberg_interaction_constant,
                spin_ring.spin,
                spin_ring.number_of_spins,
                spin_ring.anisotropy_axes_angle,
            ),
        ).fetchone()
        if row is not None:
            return row["parameter_id"]

    def create_parameter_id(self, spin_ring: SpinRing) -> int:
        self._cursor.execute(
            self._INSERT_PARAMETERS_QUERY,
            (
                spin_ring.magnetic_field_of_first_spin[indices_mapping["x"]],
                spin_ring.magnetic_field_of_first_spin[indices_mapping["y"]],
                spin_ring.magnetic_field_of_first_spin[indices_mapping["z"]],
                spin_ring.magnetic_field_type,
                spin_ring.heisenberg_interaction_constant,
                spin_ring.spin,
                spin_ring.number_of_spins,
                spin_ring.anisotropy_axes_angle,
            ),
        )
        self._connection.commit()
        if self._cursor.lastrowid is not None:
            return self._cursor.lastrowid
        else:
            raise Exception("ID of last row does not exist")

    def set_npy_data_paths(self, parameter_id: int, data_paths: NpyDataPaths) -> None:
        self._cursor.execute(
            self._UPDATE_DATA_PATHS_QUERY,
            (
                parameter_id,
                data_paths.x_values_path,
                data_paths.eigenvalues_path,
                data_paths.eigenvectors_path,
            ),
        )

    def get_npy_data_paths(self, parameter_id: int) -> NpyDataPaths:
        row = self._cursor.execute(self._GET_DATAPATHS_QUERY, (parameter_id,)).fetchone()
        if row is None:
            raise Exception("Parameter ID does not exist")
        return NpyDataPaths(
            x_values_path=row["x_values_npy_path"],
            eigenvalues_path=row["eigenvalues_npy_path"],
            eigenvectors_path=row["eigenvectors_npy_path"],
        )
