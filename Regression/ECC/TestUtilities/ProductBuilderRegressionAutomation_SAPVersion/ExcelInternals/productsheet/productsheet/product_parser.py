import logging
from collections import OrderedDict
from openpyxl import load_workbook

logger = logging.getLogger(__name__)


class ExcelReader:
    def __init__(self, fp):
        self.fp = fp
        self.workbook = load_workbook(fp, read_only=False)
        self.worksheet = self.workbook.active
        self.header_names = None
        self.data_validations = self.worksheet.data_validations
        self.valid_values_lists = {}
        self.row_num = 0
        self.blank_row_count = 0

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

    def get_valid_values_for(self, field_name):
        return self.valid_values_lists[field_name]

    def _get_list_validation_values(self, list_name):
        # https://openpyxl.readthedocs.io/en/stable/defined_names.html
        action_range = self.workbook.defined_names[list_name]
        sheet_name, cell_range_coord = next(action_range.destinations)
        data = self.workbook[sheet_name][cell_range_coord]
        if type(data) != tuple:
            r = []
            r.append(data.value)
            return r
        values = [clu[0].value for clu in data]
        return values

    def _extract_validation_lists(self, row_):
        for i, col in enumerate(row_):
            validator = self._get_validator(col)
            if not validator or validator.validation_type != "list":
                continue
            valid_values = self._get_list_validation_values(validator.formula1)
            self.valid_values_lists[self.header_names[i]] = valid_values

    def _get_validator(self, cell):
        for dv in self.data_validations.dataValidation:
            if cell in dv:
                return dv
        return None

    def _safe_get_val(self, obj):
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
            header_row = next(rows)
        except StopIteration:
            return

        self.header_names = [self._safe_get_val(cell) for cell in header_row]
        self.row_num += 1

        for row in rows:
            values = []
            for col in row:
                values.append(self._safe_get_val(col))

            if self.row_num == 1:
                self._extract_validation_lists(row)

            self.row_num += 1

            # get rid of rows with all blank cells
            if not list(filter(None, values)):
                self.blank_row_count += 1
                continue

            if self.header_names and len(self.header_names) > 0:
                yield OrderedDict(zip(self.header_names, values))
            else:
                yield values


if __name__ == "__main__":
    with open("Products_7_31_2019.xlsx", "rb") as fp:
        rdr = ExcelReader(fp)
        for row in rdr.get_rows():
            print(str(row))

        print("{}: {}".format("Action", rdr.get_valid_values_for("Action")))
        print("{}: {}".format("ChannelSlug", rdr.get_valid_values_for("ChannelSlug")))
        print("{}: {}".format("PartnerCode", rdr.get_valid_values_for("PartnerCode")))
