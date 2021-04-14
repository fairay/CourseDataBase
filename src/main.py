from inject_module import *
from src.repository import acc_rep

if __name__ == '__main__':
    acc = inject.instance(acc_rep.AccountsRepository)  # pers_rep.PWPersonRep()
    pers_arr = acc.get()
