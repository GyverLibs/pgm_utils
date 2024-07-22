num = 512

txt = """
#pragma once
#define PU_EXP(x) x
#define PU_CONCAT(x, y) PU_CONCAT_IMPL(x, y)
#define PU_CONCAT_IMPL(x, y) x##y

#define PU_FOR_NARG(...) PU_FOR_NARG_(__VA_ARGS__, PU_FOR_RSEQ_N())
#define PU_FOR_NARG_(...) PU_EXP(PU_FOR_ARG_N(__VA_ARGS__))

#define PU_FOR_ARG_N("""

for i in range(1, num):
    txt += f"_{i}, "

txt += """N, ...) N
#define PU_FOR_RSEQ_N() """

for i in range(0, num):
    txt += f"{num - i - 1}, "

txt += '\n'

for i in range(0, num):
    txt += f"\n#define PU_FOR_{i + 1}(f, N, p, x, ...) f(N, {i}, p, x)"
    if (i): txt += f" PU_EXP(PU_FOR_{i}(f, N, p, __VA_ARGS__))"

txt += """

#define PU_FOR_(N, f, p, ...) PU_EXP(PU_CONCAT(PU_FOR_, N)(f, N, p, __VA_ARGS__))
#define PU_FOR(f, p, ...) PU_FOR_(PU_FOR_NARG(__VA_ARGS__), f, p, __VA_ARGS__)
"""

print(txt)