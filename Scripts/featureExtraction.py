import pandas as pd
import re


# Feature Extract Functions
# Length
def InLength(s):
    return len(str(s))

# Presence of SQL keywords
def InKeywords(s):
    keywords = ["select", "insert", "update", "delete", "drop", "truncate", "union", "from", "where", "order by", "group by", "having", "limit", "offset", "join", "on", "and", "or", "not", "like", "in", "exists", "create", "alter", "grant", "revoke", "exec" , "sleep"]
    count = sum(keyword in str(s).lower() for keyword in keywords)
    return count

# Frequency of SQL keywords
def KeywordsFreq(s):
    count = InKeywords(s)
    return (count / len(s)) * 100

# Use of special characters
def InSpcChars(s):
    special_chars = ['"', "'", ";", "(", ")", "/", "*", "=", "<", ">", "@", "#", "$", "^", "!", "%", "&", "?"]
    count = sum(c in special_chars for c in str(s))
    return count

# Presence of comment symbols
def InComment(s):
    comment_syms = ["--", "/*", "*/"]
    count = sum(c in comment_syms for c in str(s))
    return count

# Presence of wildcards
def InWildcards(s):
    wildcards = ["%", "_", "[", "]", "^", "[^]"]
    count = sum(c in wildcards for c in str(s))
    return count

# Presense of escape characters
def InEscape(s):
    escape_chars = ['"', "'", "%", "\n", "\r", "\t", "\'", '\"', "\\", "\b", "\f"]
    count = sum(c in escape_chars for c in str(s))
    return count

# Frequency of special characters and combinations
def SpcCharsFreq(s):
    strs = ['"', "'", ";", "(", ")", "/", "*", "=", "<", ">", "@", "#", "$", "^", "!", "&", "?", "--", "/*", "*/", '"', "'", "%", "\n", "\r", "\t", "\'", '\"', "\\", "\b", "\f", "_", "[", "]", "[^]"]
    count = sum (c in strs for c in str(s))
    return (count / len(str(s))) * 100

# Known SQL Injection attack strings or patterns
def union_str(s):
    if "union select" in str(s).lower() \
        or "union all select" in str(s).lower() \
        or "union select null" in str(s).lower() \
        or "union select concat" in str(s).lower():
        return 1
    else:
        return 0
    
def errorBase_str(s):
    if "SELECT * FROM table WHERE id='1' AND 1=1 UNION SELECT 1, @@version--" in str(s) \
        or "SELECT * FROM table WHERE id='1' AND 1=1 UNION SELECT 1, column_name FROM information_schema.columns--" in str(s):
        return 1
    else:
        return 0

def bool_str(s):
    if "where id = '1'" in str(s).lower() \
        or "where username = 'admin'" in str(s).lower() \
        or "where username = 1" in str(s).lower() \
        or "or 1 = 1" in str(s).lower() \
        or "or '1' = '1'" in str(s).lower() \
        or "or a = a" in str(s).lower() \
        or "or 'a' = 'a'" in str(s).lower() \
        or "or 2 between 1 and 3" in str(s).lower() \
        or "'' = ''":
        return 1
    else:
        return 0
    
# Use of time-based SQL injection techniques
def timeBase_str(s):
    # List of time-based SQL injection keywords and functions
    time_keywords = ['SLEEP', 'BENCHMARK', 'WAITFOR', 'DELAY', 'PAUSE']
    time_functions = ['RAND()', 'SLEEP()', 'BENCHMARK()', 'WAITFOR()', 'DELAY()', 'PAUSE()']

    # Define the regular expression pattern to search for
    time_pattern = r'\b({})\b|\b({})\('.format('|'.join(time_keywords), '|'.join(time_functions))

    query = str(s)
    # Search for time-based patterns in the query
    match = re.search(time_pattern, query, re.IGNORECASE)
    
    # If a time-based pattern is found, return 1, otherwise 0
    if match:
        return 1
    else:
        return 0
    
# Number of parameters in a query
def InParam(s):
    param_patt = re.compile(r'\?')
    query = str(s)
    count = len(param_patt.findall(str(s)))
    return count

# Use of encoding to hide the attack
def InEncoding(s):
    encoding_techniques = ['hex', 'unicode', 'base64', 'url encoding', 'html encoding']
    count = 0
    for technique in encoding_techniques:
        # Check if the technique is present in the sentence
        if re.search(technique, str(s), re.IGNORECASE):
            count += 1
    return count

#  Presence of error messages or unexpected behavior
def errorMess(s):
    error_pattern = r"(error|warning|unexpected|invalid|failed|syntax|not found|not exist)"
    response = str(s).lower()
    # Count the number of matches to the error pattern
    count = len(re.findall(error_pattern, str(response)))
    return count

# Use of stored procedures or functions
def storedProc(s):
    stored_proc_pattern = r"\b(?:EXEC(?:UTE)?|CALL|BEGIN|WITH\s+\w+\s+AS)\b"
    matches = re.findall(stored_proc_pattern, str(s), re.IGNORECASE)
    return len(matches)

# Presence of unusual characters such as whitespace, tabs, or line breaks
def unusualChars(s):
    count = 0
    for char in s:
        if char in [" ", "\t", "\n"]:
            count += 1
            return count
        
# Presence of subqueries of nested queries
def hasSubquery(s):
    count = 0
    if re.search(r"\b(SELECT\b.*\bFROM\b)", str(s), re.IGNORECASE):
        count = 1
    
    return count

#Presence of multiple queries in a single statement
def hasMulquery(s):
    res = 0
    if ';' in s:
        queries = str(s).lower().strip().split(';')
        count = len([q for q in queries if q.strip() != ''])
        if count > 1:
            res = 1
    return res

# Use of conditional statements
def condition_stm(s):
    regex = re.compile(r'\b(IF|THEN|ELSE)\b', re.IGNORECASE)
    # count the number of matches
    count = len(regex.findall(str(s)))
    return count

# Presence of HTML, JavaScript or other web-related code in the query
def webRelated(s):
    web_regex = r'<script>|</script>|<html>|</html>|<iframe>|</iframe>|<form>|</form>|<input>|</input>|<textarea>|</textarea>|<body>|</body>|<head>|</head>|<meta>|</meta>|<link>|</link>|<style>|</style>|<title>|</title>|<svg>|</svg>|<img>|</img>|<embed>|</embed>|<object>|</object>|<applet>|</applet>|<audio>|</audio>|<video>|</video>|<source>|</source>|<canvas>|</canvas>|<svg>|</svg>|<math>|</math>|<table>|</table>|<td>|</td>|<tr>|</tr>|<thead>|</thead>|<tbody>|</tbody>|<tfoot>|</tfoot>|<th>|</th>|<caption>|</caption>|<ul>|</ul>|<ol>|</ol>|<li>|</li>|<dl>|</dl>|<dt>|</dt>|<dd>|</dd>|<menu>|</menu>|<command>|</command>|<header>|</header>|<nav>|</nav>|<section>|</section>|<article>|</article>|<aside>|</aside>|<footer>|</footer>|<details>|</details>|<summary>|</summary>|<mark>|</mark>|<center>|</center>|<font>|</font>|<u>|</u>|<i>|</i>|<b>|</b>|<s>|</s>|<tt>|</tt>|<big>|</big>|<small>|</small>|<strike>|</strike>|<sup>|</sup>|<sub>|</sub>|<em>|</em>|<strong>|</strong>|<cite>|</cite>|<q>|</q>|<dfn>|</dfn>|<abbr>|</abbr>|<acronym>|</acronym>|<code>|</code>|<kbd>|</kbd>|<samp>|</samp>|<var>|</var>|<pre>|</pre>|<plaintext>|</plaintext>|<listing>|</listing>|<xmp>|</xmp>|<xml>|</xml>|<iframe>|</iframe>|<noscript>|</noscript>|<noembed>|</noembed>|<marquee>|</marquee>|<blink>|</blink>|<ilayer>|</ilayer>|<layer>|</layer>|<basefont>|</basefont>|<base>|</base>|<html>|</html>|<body>|</body>|<head>|</head>'
    if re.search(web_regex, str(s)):
        return 1
    else:
        return 0
    
# Presence of comments or strings that contain unusual or unexpected content
def has_unusual_content(s):
    # Look for comments
    if re.search(r'/\*.*\*/', str(s)):
        return 1
    
    # Look for strings that contain unusual or unexpected content
    unusual_content = ['../', '\\\\', 'SELECT', 'UNION', 'DROP', 'DELETE', 'TRUNCATE', 
                       'INSERT', 'UPDATE', 'EXEC', 'SCRIPT', 'SOURCE', 'COOKIE', 
                       'SESSION', 'FILE', 'SYS', 'CONFIG', 'NET']
    for content in unusual_content:
        if re.search(content, str(s), re.IGNORECASE):
            return 1
    return 0

# Use of binary data or other encoded data in the query
def binary_data_feature(s):
    # Regular expression to match base64 or hex encoded data
    regex = re.compile(r'(?:[A-Fa-f0-9]{2}){2,}|(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')

    # Search for matches in the query
    matches = regex.findall(str(s))

    # Return 1 if matches are found, 0 otherwise
    if matches:
        return True
    else:
        return False
    
# Use of database-specific functions or commands
def db_specific(s):
    # Define a list of database-specific function or command names
    db_funcs = ["LOAD_FILE", "DBMS_ASSERT", "DBMS_PIPE", "DBMS_UTILITY", "UTL_HTTP", "UTL_ENCODE", "UTL_RAW", "CTXSYS", "DBA_USERS", "USER_USERS", "SYS_CONTEXT", "DBMS_LDAP", "DBMS_CRYPTO", "DBMS_SQL", "DBMS_JOB", "DBMS_METADATA"]
    
    # Search for function or command names within the query
    for func in db_funcs:
        if re.search(r"\b{}\(".format(func), str(s)):
            return 1
    return 0

# Use of HTTP headers or cookies in the query
def count_http_headers(s):
    # Count the number of HTTP headers in a SQL query.
    pattern = r"(?i)HTTP_[A-Z_]+"
    headers = re.findall(pattern, str(s))
    return len(headers)

def count_cookies(s):
    # Count the number of cookies in a SQL query.
    pattern = r"(?i)COOKIE\("
    cookies = re.findall(pattern, str(s))
    return len(cookies)

# Presence of HTTP GET or POST requests
def hasHTTP_Request(s):
    requests = ["get", "post"]
    count = sum (c in requests for c in str(s))
    return count


# Extract to vector
def featureExtr(s):
    features = []
    features.append(InLength(s)) #1
    features.append(InKeywords(s)) #2
    features.append(KeywordsFreq(s)) #3
    features.append(InSpcChars(s)) #4
    features.append(InComment(s)) #5
    features.append(InWildcards(s)) #6
    features.append(InEscape(s)) #7
    features.append(SpcCharsFreq(s)) #8
    features.append(union_str(s)) #9
    features.append(errorBase_str(s)) #10
    features.append(bool_str(s)) #11
    features.append(timeBase_str(s)) #12
    features.append(InParam(s)) #13
    features.append(InEncoding(s)) #14
    features.append(errorMess(s)) #15
    features.append(storedProc(s)) #16
    features.append(unusualChars(s)) #17
    features.append(hasSubquery(s)) #18
    features.append(hasMulquery(s)) #19
    features.append(condition_stm(s)) #20
    features.append(has_unusual_content(s)) #21
    features.append(binary_data_feature(s)) #22
    features.append(db_specific(s)) #23
    features.append(count_http_headers(s)) #24
    features.append(count_cookies(s)) #25
    features.append(hasHTTP_Request(s)) #26
    features.append(webRelated(s)) #27
    return features
    
# Extract to vector with label
def featureExtr2(s, label):
    features = []
    features.append(InLength(s)) #1
    features.append(InKeywords(s)) #2
    features.append(KeywordsFreq(s)) #3
    features.append(InSpcChars(s)) #4
    features.append(InComment(s)) #5
    features.append(InWildcards(s)) #6
    features.append(InEscape(s)) #7
    features.append(SpcCharsFreq(s)) #8
    features.append(union_str(s)) #9
    features.append(errorBase_str(s)) #10
    features.append(bool_str(s)) #11
    features.append(timeBase_str(s)) #12
    features.append(InParam(s)) #13
    features.append(InEncoding(s)) #14
    features.append(errorMess(s)) #15
    features.append(storedProc(s)) #16
    features.append(unusualChars(s)) #17
    features.append(hasSubquery(s)) #18
    features.append(hasMulquery(s)) #19
    features.append(condition_stm(s)) #20
    features.append(has_unusual_content(s)) #21
    features.append(binary_data_feature(s)) #22
    features.append(db_specific(s)) #23
    features.append(count_http_headers(s)) #24
    features.append(count_cookies(s)) #25
    features.append(hasHTTP_Request(s)) #26
    features.append(webRelated(s)) #27

    features.append(label)
    return features





