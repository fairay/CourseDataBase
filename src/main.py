from inject_module import *
from src.repository import acc_rep, pers_rep
from src.objects.account import *
from copy import *


def _main():
    rep_acc = inject.instance(pers_rep.PersonRepository)

    old_acc = Account(login='katya_super10', perstype='test10', salt='asca12e01dqac2e', hashedpassword='2ccq0sc14qa2sdca')
    new_acc = old_acc.clone()
    new_acc.set_pers_type('test')

    acc_arr = rep_acc.get_all()
    print(acc_arr[0].get_title())
    for a in acc_arr:
        print(a)
    print("==-==" * 30, '\n'*4)

    #rep_acc.create(old_acc)

    print("==-==" * 30)
    acc_arr = rep_acc.get_all()
    print(acc_arr[0].get_title())
    for a in acc_arr:
        print(a)


if __name__ == '__main__':
    _main()