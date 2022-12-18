from math import floor

standard_formats = {
    (89, 49): 1,
    (100, 70): 1.5,
    (105, 148): 3,
    (210, 100): 4,
    (210, 148): 6,
    (210, 200): 8,
    (210, 297): 12,
    (420, 297): 24
}


def calculate_format(file_size: tuple) -> int or float:
    width, height = file_size
    width = (width / 89, width / 49)
    height = (height / 49, height / 89)
    result = max(width[0] * height[0], width[1] * height[1])
    return floor(result) if result > 1 else 1 if result > 0.5 else 0.5


structure = {
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
