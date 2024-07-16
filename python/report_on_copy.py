import torch

copy_ops = sorted(i for i in dir(torch) if not i.startswith('_') and i.endswith('_copy'))
copy_torch = [i for i in copy_ops if hasattr(torch, i[:-5])]
copy_tensor = [i for i in copy_ops if hasattr(torch.Tensor, i[:-5])]
TENSOR = torch.randn(3, 3)
COMPLEX = {} # 'complex'
TUPLE_OUT = {'split_with_sizes': 2, 'split': 2, 'unbind': 3}

ARGS = {
    'as_strided': ((2, 2), (2, 1), 1),
    'expand': ((3, 3, 3),),
    'index': (1, torch.tensor([0, 2, 1]), torch.rand(3, 3)),
    'narrow': (1, 0, 1),
    'permute': ((1, 0),),
    'select': (1, 2),
    'slice': (0,),
    'split': (1,),  # tuple
    'split_with_sizes': ((1, 2),),  # https://github.com/pytorch/pytorch/issues/58181 # tuple
    'transpose': (1, 0),
    'unfold': (1, 2, 1),
    'unsqueeze': (1,),
    'view': ((9, 1),),
}


def print_help():
    for c in copy_ops:
        print('****', c)
        help(getattr(torch, c))
        if c in copy_torch:
            print('torch:')
            help(getattr(torch, c[:-5]))
        elif c in copy_tensor:
            print('tensor:')
            help(getattr(torch.Tensor, c[:-5]))
        else:
            print('None')


def run_items():
    for c in copy_ops:
        base = c[:-5]
        if 'indices' in c or c == 'values_copy':
            # it's sparse
            continue
        if 'complex' in c or 'real' in c:
            continue

        args = ARGS.get(base, ())
        op = getattr(torch, c)
        print(c, *args)

        # Without out=
        op(TENSOR, *args)

        out_size = TUPLE_OUT.get(base)
        if out_size:
            # Out should be a tuple
            pass
        else:
            # Empty out
            out = op(TENSOR, *args, out=torch.tensor([]))
            # print(out)

            # Empty out, wrong size
            t = torch.tensor([], dtype=torch.int32)
            out = op(TENSOR, *args, out=t)

run_items()
