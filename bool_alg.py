import csv


class BoolIter:
    def __init__(self, bits, start=0, end=0):
        assert bits >= 0
        self.start = max(start, 0)
        if end > 0:
            self.end = end
        else:
            self.end = (1 << bits) - 1
        self.length = bits
        self.current = start
        self.next = start

    def __len__(self):
        return self.length

    def __next__(self):
        if self.next > self.end:
            raise StopIteration

        self.current = self.next
        self.next = self.current + 1
        binbool = list(map(lambda x: x == '1', bin(self.current)[2:]))
        return [False] * (self.length - len(binbool)) + binbool

    def __iter__(self):
        self.current = None
        self.next = self.start
        return self


class BoolBin:
    def __init__(self):
        pass

    def fprint(self, s: str, length: int, tight: bool = False):
        length = max(len(s), length)

        if tight and length == 2:
            length += 1
        elif not tight and length == 1:
            length += 1
        elif length >= 2:
            length += 2

        s += " " * (length - len(s))
        print(s, end="")

    def csv_truth_table(self, n, filepath, *args, **kwargs):
        assert n > 0
        try:
            variables = kwargs['vars']
        except KeyError:
            variables = [chr(ord('a') + x) for x in range(n)]
        assert_equal = kwargs.get('check_equal', False)
        rep_table = {
            "boolean": {
                True: "True",
                False: "False",
            },
            "bits": {
                True: "1",
                False: "0"
            },
            "short": {
                True: "T",
                False: "F",
            }
        }
        rep = kwargs.get('rep', 'boolean')

        with open(filepath, 'w', encoding="utf-8", newline='') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            function_names = [function.__name__ for function in args]
            header = variables + function_names

            if assert_equal:
                header.append("assert")

            writer.writerow(header)

            it = BoolIter(n)
            for combo in it:
                row = []
                for bit in combo:
                    row.append(rep_table[rep][bit])

                trues = 0
                for function in args:
                    res = f(*combo)
                    trues += int(res)
                    row.append(rep_table[rep][res])

                if assert_equal:
                    if trues == 0 or trues == len(args):
                        row.append(rep_table[rep][trues == 0 or trues == len(args)])
                writer.writerow(row)

    def truth_table(self, n, *args, **kwargs):
        assert n > 0
        try:
            variables = kwargs['vars']
        except KeyError:
            variables = [chr(ord('a') + x) for x in range(n)]

        assert_equal = kwargs.get('check_equal', False)
        variables[-1] += " "
        rep_table = {
            "boolean": {
                True: "True",
                False: "False",
            },
            "bits": {
                True: "1",
                False: "0"
            },
            "short": {
                True: "T",
                False: "F",
            }
        }
        rep = kwargs.get('rep', 'boolean')

        bool_len = len(rep_table[rep][False])
        col_len = max(bool_len, max(len(f.__name__) for f in args))

        print("Truth Table:")
        for var in variables:
            self.fprint(var, bool_len, tight=True)

        for function in args:
            self.fprint(function.__name__, max(col_len, bool_len), tight=False)

        if assert_equal:
            print("Assert")
        else:
            print()

        it = BoolIter(n)
        for combo in it:
            i = 0
            for bit in combo:
                self.fprint(rep_table[rep][bit], max(len(variables[i]), bool_len), tight=True)
                i += 1

            trues = 0
            for function in args:
                res = function(*combo)
                trues += int(res)
                self.fprint(rep_table[rep][res], max(col_len, len(function.__name__)), tight=False)

            if not assert_equal:
                print("")
                continue

            if trues == 0 or trues == len(args):
                print(rep_table[rep][True])
            else:
                print(rep_table[rep][False])

    def print_k_map(self, kmap, left, top, n, m):
        x_len = len(kmap[0]) * 4
        top = top.center(x_len)
        num_size = 2
        l_space = ' ' * (len(left) + num_size + n)
        gray_code = [[], ["0", "1"], ["00", "01", "11", "10"]]
        print(l_space, end="")
        print(top)
        print(l_space, end="")
        if m == 2:
            header = "  ".join(gray_code[m])
            print(f"\033[4m {header}\033[0m")
        elif m == 1:
            header = "   ".join(gray_code[m])
            print(f"\033[4m {header} \033[0m")

        mid = len(kmap) // 2
        for i, row in enumerate(kmap):
            if i == mid:
                print(left, end=" ")
            else:
                print(' ' * (len(left) + 1), end="")
            print(f"{gray_code[n][i]}|", end="")

            for num in row:
                print(f"\033[4m {num} \033[0m", end="")
                print("|", end="")
            print()

    def kmap(self, vars, minterms, label_left="", label_top="", n=None, m=None):
        mx = max(minterms)
        mn = min(minterms)
        assert mx < (1 << vars)
        assert mn >= 0
        partion2 = vars // 2
        partion1 = vars - partion2
        if n and m:
            assert n + m == vars
            partion1 = m
            partion2 = n
        gray_code = [0, 1, 3, 2]
        kmap = [[0 for j in range((1 << partion1))] for i in range((1 << partion2))]
        for term in minterms:
            bterm = bin(term)[2:]
            bterm = (vars - len(bterm)) * "0" + bterm
            key1 = bterm[0:partion1]
            key2 = bterm[partion1:]
            kmap[gray_code[int(key2, 2)]][gray_code[int(key1, 2)]] = 1
        self.print_k_map(kmap, label_left, label_top, partion2, partion1)

    def f_kmap(self, f, variables, l1, l2):
        ordered_vars = l1 + l2
        n = len(variables)

        assert n == len(ordered_vars)
        assert sorted(ordered_vars) == sorted(variables)

        mapping = {}
        shifts = [0 for _ in range(n)]

        for i in range(n):
            mapping[variables[i]] = i

        for i in range(len(variables)):
            shifts[mapping[ordered_vars[i]]] = n - i - 1

        minterms = []
        it = BoolIter(n)
        for combo in it:
            if not f(*combo):
                continue
            idx = 0
            for bit, shift in zip(combo, shifts):
                idx += (int(bit) << shift)
            minterms.append(idx)
        print(f"{f.__name__}:")
        self.kmap(n, minterms, "".join(l2), "".join(l1), len(l2), len(l1))


class WeightedSum:
    def __init__(self, weights):
        self.weights = weights
        self.sorted_weights = sorted(weights)
        self.max = sum(self.weights)
        self.rep, self.lookup = self.build_cover()
        self.max_cont = self.patch()

    def build_cover(self):
        rep = {}
        lookup = {}
        for i in range(1 << len(self.weights)):
            sm = 0
            for shift in range(len(self.weights)):
                if i & (1 << shift):
                    idx = len(self.weights) - 1 - shift
                    sm += self.weights[idx]

            # How each number is represented
            rep.setdefault(sm, []).append(i)
            # Value of each weighted sum
            lookup[i] = sm
        return rep, lookup

    def patch(self):
        mx = 0
        i = 0
        while i < len(self.weights) and self.sorted_weights[i] <= mx + 1:
            mx += self.sorted_weights[i]
            i += 1
        return mx

    def is_covered(self, n):
        return n in self.rep

    def max_continous_coverage(self, n):
        return self.max_cont

    def max_number(self, n):
        return self.max

    def calc_sum_bin(self, s):
        n = int(s, 2)
        return self.calc_sum(n)

    def calc_sum(self, n):
        if n >= (1 << len(self.weights)):
            raise ValueError

        return self.lookup[n]

    def calc_sum_arr(self, arr):
        digits = list(map(lambda x: str(int(bool(x))), arr))
        n = int("".join(digits), 2)
        return self.calc_sum(n)

    def representation(self, n):
        return self.rep.get(n, None)


class MTerm:
    def __init__(self, vars):
        self.vars = vars
        self.params = ",".join(vars)
        self.length = len(vars)
        self.max = (1 << self.length)
        self.min = 0

    def bin_all(self, nums):
        ans = []
        for num in nums:
            if num >= self.max or num < self.min:
                raise ValueError
            nb = bin(num)[2:]
            nb = (self.length - len(nb)) * "0" + nb
            ans.append(nb)
        return ans

    def list_complement(self, terms):
        terms.sort()
        new_terms = []
        idx = 0
        for i in range(self.max):
            while idx < len(terms) and i > terms[idx]:
                idx += 1
            if idx < len(terms) and i == terms[idx]:
                continue
            else:
                new_terms.append(i)
        return new_terms

    def expand_min(self, terms, f="f", max=False):
        if max:
            terms = self.list_complement(terms)

        ans = ""
        for term in terms:
            if term >= self.max or term < self.min:
                raise ValueError

            nb = bin(term)[2:]
            nb = (self.length - len(nb)) * "0" + nb
            t = []
            for i, bit in enumerate(nb):
                if bit == '0':
                    t.append(f"{self.vars[i]}'")
                else:
                    t.append(f"{self.vars[i]} ")
            ans += "".join(t) + " + "

        ans = ans[:-3]
        result = f"{f}({self.params}) = "
        print(result)
        print(ans)

    def expand_max(self, terms, f="f", min=False):
        if min:
            terms = self.list_complement(terms)

        ans = ""
        for term in terms:
            if term > self.max or term < self.min:
                raise ValueError

            nb = bin(term)[2:]
            nb = (self.length - len(nb)) * "0" + nb
            t = []
            for i, bit in enumerate(nb):
                if bit == '0':
                    t.append(self.vars[i])
                else:
                    t.append(self.vars[i] + "'")
            ans += "(" + " + ".join(t) + ") "

        result = f"{f}({self.params}) = "
        print(result)
        print(ans)
