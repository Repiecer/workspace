class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        if len(strs) == 1:
            return strs[0]
        main_str = strs[0]
        for s in strs[1:]:
            main_str = main_str[:len(main_str)-len(s)]
            
            