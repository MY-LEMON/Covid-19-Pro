# FLASK后端

## 问答系统



**def build_actree:**

该函数构建领域actree，加速过滤。通过python的ahocorasick库实现。
ahocorasick是一种字符串匹配算法，由两种数据结构实现：trie和Aho-Corasick自动机。
Trie是一个字符串索引的词典，检索相关项时时间和字符串长度成正比。
AC自动机能够在一次运行中找到给定集合所有字符串。AC自动机其实就是在Trie树上实现KMP，可以完成多模式串的匹配。

