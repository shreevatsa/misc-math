import math
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rc('text', usetex=True)

of = open('bins-n2-21n-1.txt').readlines()
og = open('bins-n2-n-1.txt').readlines()
print(len(of), len(og))
NUM_BINS = 1000
MAX_VALUE = 1000000000
BIN_SIZE = MAX_VALUE / NUM_BINS
assert len(of) == len(og) == NUM_BINS * 10

f = [sum(int(of[i]) for i in range(n, n + 10)) for n in range(NUM_BINS)]
g = [sum(int(og[i]) for i in range(n, n + 10)) for n in range(NUM_BINS)]
ratios = [float(f[i])/float(g[i]) for i in range(len(f))]
unscaled_logs = []
for n in range(NUM_BINS):
    x = (n + 1) * BIN_SIZE
    y = x / math.log(x)
    x -= BIN_SIZE
    y_prev = x/math.log(x) if n > 0 else 0
    unscaled_logs.append(y - y_prev)
gl = [y*1.25 for y in unscaled_logs]
flscaler = 2.79
fl = [y*flscaler for y in unscaled_logs]

xs = range(1, NUM_BINS + 1)
print('Done xs')

fig, ax1 = plt.subplots()

ax1.set_xlabel('Bin of size {:,}'.format(MAX_VALUE / NUM_BINS))

print('Plotting data')
linef, = ax1.plot(xs, f)
linefl,= ax1.plot(xs, fl)
lineg, = ax1.plot(xs, g)
linegl, = ax1.plot(xs, gl)
ax1.set_ylim(ymin=0)
ax1.set_xlim(xmin=0)
ax1.legend([linef, linefl, lineg, linegl],
           ['$n^2 + 21n + 1$', r'$%.2f n / \ln(n)$' % flscaler, '$n^2 + n + 1$', r'$1.25 n / \ln(n)$'],
           loc='upper right',
           # fontsize = 'small'
               )
ax1.set_ylabel('Number of primes in bin')
print('Done plotting ax1')

# print('Plotting ratio')
# ax2 = ax1.twinx()
# ax2.plot(xs, ratios, color=plt.rcParams['axes.prop_cycle'].by_key()['color'][4], label = 'Ratio')
# ax2.set_ylim(ymin=0, ymax=3)
# ax2.legend(loc='upper right', fontsize='small')
# print('Done plotting ax2')

plt.title('Primes in quadratic sequences')
plt.savefig('num_primes.png', dpi=600)
