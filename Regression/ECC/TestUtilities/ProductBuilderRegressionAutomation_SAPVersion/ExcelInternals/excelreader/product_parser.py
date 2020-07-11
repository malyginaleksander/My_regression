import logging
from openpyxl import load_workbook

logger = logging.getLogger(__name__)


class ExcelReader:
    def __init__(self, fp):
        self.fp = fp
        self.workbook = load_workbook(fp, read_only=False)
        self.worksheet = self.workbook.active
        self.data_validations = self.worksheet.data_validations

        if hasattr(fp, "name"):
            self.filename = fp.name
        elif hasattr(fp, "_name"):
            self.filename = fp._name
        else:
            logger.error(
                "cannot determine name for fp. vars: %s",
                         vars(fp)
            )
            self.filename = ""

    def get_validator(self, cell):
        for dv in self.data_validations.dataValidation:
            if cell in dv:
                return dv
        return None

    def safe_get_val(self, obj):
        if hasattr(obj, "value"):
            val = getattr(obj, "value", "")
        else:
            val = obj
        if val:
            return str(val).strip()
        else:
            return ""

    def get_rows(self):
        rows = self.worksheet.rows

        try:
            header_row = list(map(self.safe_get_val, next(rows)))
        except StopIteration:
            return

        for row in rows:
            values = []
            for col in row:
                values.append(self.safe_get_val(col))
                validator = self.get_validator(col)
                if validator:
                    logger.warning("Validation for cell '%s' is '%s'", col.coordinate, validator.error)

            # get rid of rows with all blank cells
            if not list(filter(None, values)):
                continue

            if header_row and len(header_row) > 0:
                yield dict(zip(header_row, values))
            else:
                yield values


if __name__ == "__main__":
    with open("Products_7_31_2019.xlsx", "rb") as fp:
        rdr = ExcelReader(fp)
        for row in rdr.get_rows():
            print(str(row))
