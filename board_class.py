class BoardClass():

    def __init__(self):
        self.board_dict = {'etc':'기타', 
        'game' : '게임',
        'anonymous' : '익명',
        'no-member' : '비회원'
        }

    def get_board_dict(self):
        return self.board_dict

    def get_board_name(self, en_name: str) -> str:
        return self.board_dict[en_name]

    def set_board_dict(self, en_name: str, ko_name: str) -> dict:
        self.board_dict[en_name] = ko_name

    def isNotAllowBoard(self, board: str) -> bool:
        """
        ### 허용되지 않은 게시판인지 확인
        """
        return board not in self.board_dict