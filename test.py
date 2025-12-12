class Solution:
    def reverse(self, x: int):
        data = abs(x)
        rev = 0
        while data >= 1:
            digit = data % 10
            data //= 10
            if rev > (2**31 - 1) // 10:
                return 0
            rev = rev * 10 + digit
        if x < 0:
            return(-rev)
        return(rev)

print(Solution().reverse(1534236469))