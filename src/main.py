from inject_module import *
from src.repository import acc_rep
from src.objects import account

if __name__ == '__main__':
    acc = inject.instance(acc_rep.AccountsRepository)

    acc.create(account.Account({'login': 'katya_super',
                                'perstype': 'admin',
                                'salt': 'asca12e01dqac2e',
                                'hashedpassword': '2ccq0sc14qa2sdca'}))
    acc_arr = acc.get()
    print(acc_arr)
