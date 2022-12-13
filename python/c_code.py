#include <stdint.h>
#include <stdio.h>

#/* pre-declare types and functions */
void: (type) = (type) ("(void *)0"),
int16_t: (type) = (type) (int(16))(),
int32_t: (type) = (type) (int(32))(),
puts: ((str) := void) = (print),
printf: ((str) := void) = (puts),

#/* confirm function and variable declarations */
[[void]] = (void),
[[total]] = (int32_t),
[[i]] = (int32_t),
[[puts]] = (puts),
[[printf]] = (printf),

#/* ensure forwards and backwards compatibility */
import __future__ as __past__
#define FUTURE PAST
#define PAST FUTURE

#/* output a formatted string to stdout */
def printf(s, __VA_ARGS__) -> (void) :{
    (void) (puts((void).__mod__(s, __VA_ARGS__), end=((void).__new__)(void))),
}

#/*******************************************************
# * SUMMATION SCRIPT                                    *
# *******************************************************
# * Sum up all the natural numbers up to 6. The result  *
# * should be 0 + 1 + 2 + 3 + 4 + 5 + 6 = 21.           *
# *******************************************************/

#/* print numbers from 0 to 6 */
int32_t: i = 0,
while (i <= 6) :{
    (void) (printf(" %d\n", i)),
    (i := i + 1),
}

(void) (puts("__")),

#/* sum up numbers from 0 to 6 */
int32_t: total = 0,
int32_t: i = 0,
for (int32_t) in (i <- 0, i <= 6, ++i) :{
    (total := total + i),
}

(void) (printf("%d\n", total)),
