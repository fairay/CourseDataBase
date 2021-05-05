from cite import *


def _main():
    rep_acc = inject.instance(AccountsRepository)

    old_acc = Account(login='petya_super10', perstype='test10', salt='asca12e01dqac2e', hashedpassword='2ccq0sc14qa2sdca')
    new_acc = old_acc.clone()
    new_acc.set_pers_type(None)

    acc_arr = rep_acc.get_all()
    print(acc_arr[0].get_title())
    for a in acc_arr:
        print(a)
    print("==-==" * 30, '\n'*4)

    try:
        rep_acc.update(old_acc, new_acc)
    except WrongUpdExc as exc:
        print('Беда')

    print("==-==" * 30)
    acc_arr = rep_acc.get_all()
    print(acc_arr[0].get_title())
    for a in acc_arr:
        print(a)


if __name__ == '__main__':
    _main()
