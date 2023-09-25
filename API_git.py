from github import Github
from github import PaginatedList

class ArchiveGit:
    def __init__(self,text:str) -> None:
        self.__lines = text.split("\n")
        self.__text = text
    
    def get_code_by_line(self,line_init,line_end):
        return self.__map(line_init,line_end)
    
    def have_this_line(self,line:int):
        return len(self.__lines) >= (line)
    
    def get_line_by_key(self,key:str):
        for i,line in enumerate(self.__lines):
            if key in line:
                return i
    
    def __map(self,line_init,line_fim):
        line = 0
        pos_i = None
        pos_f = None
        for i,carcter in enumerate(self.__text):
            if carcter == "\n":
                line += 1
                if line == line_init:
                    pos_i = i
                if line-1 == line_fim:
                    pos_f = i
        
        return self.__text[pos_i:pos_f]


class ArchivesGit:
    def __init__(self,list_arquives:PaginatedList):
        self.__archives = [ArchiveGit(arquive.decoded_content.decode('utf-8')) for arquive in list_arquives]
    
    def get_arquives_by_lines(self,line,limiar,key)->list[str]:
        archives = list()
        for archive in self.__archives:
            if archive.have_this_line(line):
                i = archive.get_line_by_key(key)
                if i == line - 1:
                    archives.append(archive.get_code_by_line(line-limiar,line))
        return archives

class ItauGitHub:
    def __init__(self,token_access,username):
        self.__git = Github(token_access)
        self.__user = username

    def search_on_arquives(self,query:str,line,limiar,key)->PaginatedList:
        query = f"{query} user:{self.__user}"
        return ArchivesGit(self.__git.search_code(query)).get_arquives_by_lines(line,limiar,key)
    

teste = ItauGitHub("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","Augusto-cmk")
print(teste.search_on_arquives('language:python class "MessageService"',5,5,"MessageService")[0])
        