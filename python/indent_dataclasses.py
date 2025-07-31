import token
import tokenize

INDENT = '  '


def indent_ds(s: str):
    parts = []
    indent = ''
    for t in tokenize.generate_tokens(iter(s.splitlines()).__next__):
        parts.append(t.string)
        if t.type != token.OP:
            continue

        if t.string in "([{":
            indent += INDENT
        elif t.string in ")]}":
            indent = indent[:-len(INDENT)]
        elif t.string != ",":
            continue

        parts.append(f"\n{indent}")

    print(*parts)


DATA = "NativeFunction(namespace='aten', func=FunctionSchema(name=OperatorName(name=BaseOperatorName(base='randint', inplace=False, dunder_method=False, functional_overload=False, namespace=None), overload_name=''), arguments=Arguments(pre_self_positional=(), self_arg=None, post_self_positional=(Argument(name='high', type=BaseType(name=<BaseTy.SymInt: 18>), default=None, annotation=None), Argument(name='size', type=ListType(elem=BaseType(name=<BaseTy.SymInt: 18>), size=None), default=None, annotation=None)), pre_tensor_options_kwarg_only=(), tensor_options=TensorOptionsArguments(dtype=Argument(name='dtype', type=OptionalType(elem=BaseType(name=<BaseTy.ScalarType: 2>)), default='long', annotation=None), layout=Argument(name='layout', type=OptionalType(elem=BaseType(name=<BaseTy.Layout: 10>)), default='None', annotation=None), device=Argument(name='device', type=OptionalType(elem=BaseType(name=<BaseTy.Device: 11>)), default='None', annotation=None), pin_memory=Argument(name='pin_memory', type=OptionalType(elem=BaseType(name=<BaseTy.bool: 9>)), default='None', annotation=None)), post_tensor_options_kwarg_only=(), out=()), returns=(Return(name=None, type=BaseType(name=<BaseTy.Tensor: 3>), annotation=None),)), use_const_ref_for_mutable_tensors=False, device_guard=True, device_check=<DeviceCheckType.ExactSame: 1>, python_module=None, category_override=None, variants={<Variant.function: 1>}, manual_kernel_registration=False, manual_cpp_binding=False, loc=Location(file=PosixPath('/home/rec/git-typing/pytorch/aten/src/ATen/native/native_functions.yaml'), line=4744), autogen=[], ufunc_inner_loop={}, structured=False, structured_delegate=None, structured_inherits=None, precomputed=None, cpp_no_default_args=set(), is_abstract=True, has_composite_implicit_autograd_kernel=False, has_composite_implicit_autograd_nested_tensor_kernel=False, has_composite_explicit_autograd_kernel=True, has_composite_explicit_autograd_non_functional_kernel=False, tags={'nondeterministic_seeded', 'pt2_compliant_tag'})"


indent_ds(DATA)
