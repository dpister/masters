from __future__ import annotations
import sqlite3
from types import TracebackType
from typing import Any, Type

from spin_ring import SpinRing

from math_helper import indices_mapping, number


class DatabaseException(Exception):
    pass


class NoRowFoundException(DatabaseException):
    pass


class MissingValueException(DatabaseException):
    pass


class CreationException(DatabaseException):
    pass


class Database:
    """Context Manager to connect with SQLite3 Database and close connection safely"""

    def __init__(self, database_path: str):
        self._database_path = database_path

    def __enter__(self) -> Database:
        self._connection = sqlite3.connect(self._database_path)
        self._connection.row_factory = sqlite3.Row
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
    """Table that matches a combination of parameters with a parameter ID"""

    _CREATE_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS parameters (
            parameter_id INTEGER PRIMARY KEY,
            B_x REAL,
            B_y REAL,
            B_z REAL,
            B_strength REAL,
            B_type TEXT NOT NULL CHECK (B_type IN ('circular', 'linear')),
            D REAL,
            J REAL,
            s REAL,
            N INTEGER,
            D_angle REAL
        )
        """

    def __enter__(self) -> ParameterDatabase:
        super().__enter__()
        self._cursor.execute(self._CREATE_TABLE_QUERY)
        self._connection.commit()
        return self

    _GET_PARAMETER_ID_QUERY = """
        SELECT parameter_id
        FROM parameters 
        WHERE
        B_x = ? AND
        B_y = ? AND
        B_z = ? AND
        B_strength = ? AND
        B_type = ? AND
        D = ? AND
        J = ? AND
        s = ? AND
        N = ? AND
        D_angle = ?
        """

    def get_parameter_id(self, spin_ring: SpinRing) -> int:
        row = self._cursor.execute(
            self._GET_PARAMETER_ID_QUERY,
            (
                spin_ring.magnetic_field_direction_of_first_spin[indices_mapping["x"]],
                spin_ring.magnetic_field_direction_of_first_spin[indices_mapping["y"]],
                spin_ring.magnetic_field_direction_of_first_spin[indices_mapping["z"]],
                spin_ring.magnetic_field_strength,
                spin_ring.magnetic_field_type,
                spin_ring.anisotropy_value,
                spin_ring.heisenberg_interaction_constant,
                spin_ring.spin,
                spin_ring.number_of_spins,
                spin_ring.anisotropy_axes_angle,
            ),
        ).fetchone()
        if row is None:
            raise NoRowFoundException("No row found with the spin ring's parameters")
        parameter_id: int = self._get_row_data(row, "parameter_id")
        return parameter_id

    _INSERT_PARAMETERS_QUERY = """
        INSERT INTO parameters (
            B_x,
            B_y,
            B_z,
            B_strength,
            B_type,
            D,
            J,
            s,
            N,
            D_angle
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

    def create_parameter_id(self, spin_ring: SpinRing) -> int:
        self._cursor.execute(
            self._INSERT_PARAMETERS_QUERY,
            (
                spin_ring.magnetic_field_direction_of_first_spin[indices_mapping["x"]],
                spin_ring.magnetic_field_direction_of_first_spin[indices_mapping["y"]],
                spin_ring.magnetic_field_direction_of_first_spin[indices_mapping["z"]],
                spin_ring.magnetic_field_strength,
                spin_ring.magnetic_field_type,
                spin_ring.anisotropy_value,
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
            raise CreationException()

    def _get_row_data(self, row: sqlite3.Row, column: str) -> Any:
        return_value = row[column]
        if return_value is None:
            raise MissingValueException(f'Missing data for column "{column}"')
        return return_value

    _GET_PARAMETER_IDS_BY_ANGLE_INTERVAL_QUERY = """
        SELECT parameter_id, D_angle
        FROM parameters
        WHERE 
        B_x = ? AND
        B_y = ? AND
        B_z = ? AND
        B_strength = ? AND
        B_type = ? AND
        D = ? AND
        J = ? AND
        s = ? AND
        N = ? AND
        D_angle >= ? AND 
        D_angle <= ?
    """

    def get_entries_by_angle_interval(
        self, min_angle: number, max_angle: number, spin_ring: SpinRing
    ) -> list[tuple[int, number]]:
        rows = self._cursor.execute(
            self._GET_PARAMETER_IDS_BY_ANGLE_INTERVAL_QUERY,
            (
                spin_ring.magnetic_field_direction_of_first_spin[indices_mapping["x"]],
                spin_ring.magnetic_field_direction_of_first_spin[indices_mapping["y"]],
                spin_ring.magnetic_field_direction_of_first_spin[indices_mapping["z"]],
                spin_ring.magnetic_field_strength,
                spin_ring.magnetic_field_type,
                spin_ring.anisotropy_value,
                spin_ring.heisenberg_interaction_constant,
                spin_ring.spin,
                spin_ring.number_of_spins,
                min_angle,
                max_angle,
            ),
        ).fetchall()
        return [(self._get_row_data(row, "parameter_id"), self._get_row_data(row, "D_angle")) for row in rows]

    _GET_PARAMETER_IDS_BY_MAGNETIC_FIELD_INTERVAL = """
        SELECT parameter_id, B_strength
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
        D_angle = ? AND 
        B_strength >= ? AND 
        B_strength <= ?
    """

    def get_entries_by_magnetic_field_interval(
        self,
        spin_ring: SpinRing,
        min_magnetic_field: number,
        max_magnetic_field: number,
    ) -> list[tuple[int, number]]:
        rows = self._cursor.execute(
            self._GET_PARAMETER_IDS_BY_MAGNETIC_FIELD_INTERVAL,
            (
                spin_ring.magnetic_field_direction_of_first_spin[indices_mapping["x"]],
                spin_ring.magnetic_field_direction_of_first_spin[indices_mapping["y"]],
                spin_ring.magnetic_field_direction_of_first_spin[indices_mapping["z"]],
                spin_ring.magnetic_field_type,
                spin_ring.anisotropy_value,
                spin_ring.heisenberg_interaction_constant,
                spin_ring.spin,
                spin_ring.number_of_spins,
                spin_ring.anisotropy_axes_angle,
                min_magnetic_field,
                max_magnetic_field,
            ),
        ).fetchall()
        return [(self._get_row_data(row, "parameter_id"), self._get_row_data(row, "B_strength")) for row in rows]
