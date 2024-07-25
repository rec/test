@register_decomposition(aten.unbind_copy)
def unbind_copy(
    t: TensorLikeType, dim: int = 0, out: Optional[TensorSequenceType] = None
) -> TensorSequenceType:
    result = unbind(t, dim)
    if out is None:
        return tuple(i.clone(memory_format=torch.contiguous_format) for i in result)
    torch._check(
        len(out) == len(result),
        f"len(out) ({len(out)}) != len(result) ({len(result)})",
    )
    for o, r in zip(out, result):
        o.copy_(r)
    return out
    PythonRefInfo(
        "_refs.unbind_copy",
        torch_opinfo_name="unbind_copy",
    ),
    OpInfo('unbind_copy',
           dtypes=all_types_and_complex_and(torch.complex32, torch.bool, torch.float16, torch.bfloat16),
           ref=reference_unbind,
           sample_inputs_func=sample_inputs_unbind,
           error_inputs_func=error_inputs_unbind,
           supports_forward_ad=True,
           supports_fwgrad_bwgrad=True,
           supports_gradgrad=True,
           supports_out=True,
           ),
