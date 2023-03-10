standard_formats = {   # (длинна, ширина): кол-во мест которое занимает изделие на печатном листе
    (49, 89): 1,       # Визитка
    (55, 85): 1,       # Евро-визитка
    (70, 100): 1.5,    # Календарик
    (105, 148): 3,     # А6
    (100, 210): 4,     # Евро-флаер
    (148, 210): 6,     # А5
    (200, 210): 8,     # Евро-буклет
    (297, 210): 12,    # А4
    (297, 420): 24     # А3
}

template_cells_structure = {   # Словарь представляет собой набор ячеек из таблицы - шаблона Excel
    250: {
        'GL1+0': {
            500: {
                24: 'B3',
                48: 'C3'
            },
            1000: {
                24: 'B4',
                48: 'C4'
            }
        },
        'UF1+0': {
            500: {
                24: 'B3',
                48: 'C3'
            },
            1000: {
                24: 'B4',
                48: 'C4'
            }
        },
        'GL1+1': {
            500: {
                24: 'D3',
                48: 'E3'
            },
            1000: {
                24: 'D4',
                48: 'E4'
            }
        },
        'MAT1+0': {
            500: {
                24: 'F3',
                48: 'G3'
            },
            1000: {
                24: 'F4',
                48: 'G4'
            }
        },
        'MAT1+1': {
            500: {
                24: 'H3',
                48: 'I3'
            },
            1000: {
                24: 'H4',
                48: 'I4'
            }
        },
        'NON': {
            500: {
                24: 'J3',
                48: 'K3'
            },
            1000: {
                24: 'J4',
                48: 'K4'
            }
        }
    },
    300: {
        'GL1+0': {
            500: {
                24: 'B9',
                48: 'C9'
            },
            1000: {
                24: 'B10',
                48: 'C10'
            }
        },
        'UF1+0': {
            500: {
                24: 'B9',
                48: 'C9'
            },
            1000: {
                24: 'B10',
                48: 'C10'
            }
        },
        'GL1+1': {
            500: {
                24: 'D9',
                48: 'E9'
            },
            1000: {
                24: 'D10',
                48: 'E10'
            }
        },
        'MAT1+0': {
            500: {
                24: 'F9',
                48: 'G9'
            },
            1000: {
                24: 'F10',
                48: 'G10'
            }
        },
        'MAT1+1': {
            500: {
                24: 'H9',
                48: 'I9'
            },
            1000: {
                24: 'H10',
                48: 'I10'
            }
        },
        'NON': {
            500: {
                24: 'J9',
                48: 'K9'
            },
            1000: {
                24: 'J10',
                48: 'K10'
            }
        }
    },
    350: {
        'GL1+0': {
            500: {
                24: 'B15',
                48: 'C15'
            },
            1000: {
                24: 'B16',
                48: 'C16'
            }
        },
        'UF1+0': {
            500: {
                24: 'B15',
                48: 'C15'
            },
            1000: {
                24: 'B16',
                48: 'C16'
            }
        },
        'GL1+1': {
            500: {
                24: 'D15',
                48: 'E15'
            },
            1000: {
                24: 'D16',
                48: 'E16'
            }
        },
        'MAT1+0': {
            500: {
                24: 'F15',
                48: 'G15'
            },
            1000: {
                24: 'F16',
                48: 'G16'
            }
        },
        'MAT1+1': {
            500: {
                24: 'H15',
                48: 'I15'
            },
            1000: {
                24: 'H16',
                48: 'I16'
            }
        },
        'NON': {
            500: {
                24: 'J15',
                48: 'K15'
            },
            1000: {
                24: 'J16',
                48: 'K16'
            }
        }
    }
}
