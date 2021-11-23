import sys, os,csv
from datetime import datetime


class Sudoku:

    def __init__(self, p_path,p_output_path):
        # Initialises the dimension i.e. n value for a n by n puzzle
        self.dim_val = None
        # Variable to store the input csv file
        self.sudo_file = None
        # Variable to store the the sudoku file path
        self.sudo_file_path = p_path
        self.sudo_output_path = p_output_path
        self.start_at_zero = True
        self.sudo_list = list()

        # self.intersecting_vals = dict()

    def read_file(self):
        # Method to read the input file

        try:
            self.sudo_file = open(self.sudo_file_path, "r")
            self.dim_val = self.sudo_file.readline()
            self.add_to_list()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, e, "\nLine No: ", exc_tb.tb_lineno)
        finally:
            self.sudo_file.close()

    def add_to_list(self):
        # Method to read the file and add
        # the values to a list
        l_sudo_list = list()
        for i_line in self.sudo_file:
            row_val = i_line.strip().split(",")
            self.sudo_list.append(tuple(row_val))
            l_sudo_list.append(row_val)

        self.sudo_list = tuple(self.sudo_list)

        self.solve(l_sudo_list, 0, 0)

    def solve(self, p_sudo_list, p_row_start, p_col_start):
        # Method to solve the sudoku puzzle
        br_loop = True
        output_list = p_sudo_list.copy()
        for i_row in range(p_row_start, len(p_sudo_list)):
            for j_col in range(p_col_start, len(p_sudo_list[i_row])):
                inter_row, inter_col = self.get_intersecting_rows_cols(i_row, j_col, output_list)
                ## Check whether the rows and columns are emtpy or has values

                if self.sudo_list[i_row][j_col] == '0' or self.sudo_list[i_row][j_col] == '' or self.sudo_list[i_row][
                    j_col] is None:
                    # print(i_row, j_col,self.sudo_list)
                    output_list[i_row][j_col],br_out = \
                        self.set_unique_cell_value(i_row, j_col, inter_row, inter_col, output_list)
                else:
                    output_list[i_row][j_col] = int(p_sudo_list[i_row][j_col])
        if not any(0 in x for x in output_list):
            self.write_output(output_list)

    def write_output(self,p_output_list):
        # Writes the output list to csv file
        l_time_stamp = str(datetime.now(tz=None)).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")
        try:
            l_output_file_path = str(self.sudo_output_path+"\output_"+l_time_stamp+".csv")
            with open(l_output_file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(p_output_list)

        except Exception as e:
            print(e)
        finally:
            csvfile.close()



    def set_unique_cell_value(self, p_row, p_col, p_inter_row, p_inter_col, p_updated_sudo_list):
        # Method that assigns a value that is unique w.r.t the intersecting row and column
        l_possible_vals = set(range(1, (int(self.dim_val) + 1)))

        l_intersecting_vals = list(p_inter_row.values()) + list(p_inter_col.values())

        l_diff = list(l_possible_vals.difference(set(l_intersecting_vals)))

        if len(l_diff) == 0:
            # Backtracking
            self.start_at_zero = False
            self.solve(p_updated_sudo_list, p_row,0)
            return 0,False
        else:
            # print(l_diff)
            if len(l_diff) >=2:
                if self.start_at_zero:
                    # print("a")
                    l_val = l_diff[0]
                else:
                    # print("b")
                    l_val = l_diff[1]
                    self.start_at_zero = True
            else:
                # print("c")
                l_val = l_diff[0]
            return l_val,True

    def get_intersecting_rows_cols(self, p_row_num, p_col_num, p_sudo_list):
        # Method to get the rows and columns that intersects with the given cell

        inter_row_list = dict()
        inter_col_list = dict()

        for i_index in range(int(self.dim_val)):

            if i_index != p_col_num:
                inter_row_list[str(p_row_num) + str(i_index)] = int(p_sudo_list[p_row_num][i_index])
            if i_index != p_row_num:
                inter_col_list[str(i_index) + str(p_col_num)] = int(p_sudo_list[i_index][p_col_num])

        # self.intersecting_vals[str(p_row_num)+str(p_col_num)] = [inter_row_list,inter_col_list]
        return inter_row_list, inter_col_list


if __name__ == '__main__':
    s = Sudoku("sudoku\input.csv","sudoku")
    s.read_file()
