right_filename_pattern = r'(?i)' \
                         r'(?P<date>\d{2}-\d{2}).*?' \
                         r'(?P<OrderID>\d+)_' \
                         r'(?P<size>\d+[xх]\d+)_' \
                         r'(?P<color>\d\+\d).*?' \
                         r'(?P<density>\d{3})_' \
                         r'(?P<lam>[a-z]{2,3}\d\+\d)?.*?' \
                         r'(?P<quantity>[\d ]{3,}).*?' \
                         r'(?P<file_format>\.pdf)'

folders_pattern = r'(?i)(GL|MAT|NON|UF) ?(1\+[10])?(?=$)'

letters_only = r'(?i)[a-z]+'
digits_only = r'\d+'
