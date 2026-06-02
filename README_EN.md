This is an automatic translation and may be incorrect in some places. See the source README and examples for authoritative information.

[![latest](https://img.shields.io/github/v/release/GyverLibs/pgm_utils.svg?color=brightgreen)](https://github.com/GyverLibs/pgm_utils/releases/latest/download/pgm_utils.zip)
[![PIO](https://badges.registry.platformio.org/packages/gyverlibs/library/pgm_utils.svg)](https://registry.platformio.org/libraries/gyverlibs/pgm_utils)
[![Foo](https://img.shields.io/badge/Website-AlexGyver.ru-blue.svg?style=flat-square)](https://alexgyver.ru/)
[![Foo](https://img.shields.io/badge/%E2%82%BD%24%E2%82%AC%20%D0%9F%D0%BE%D0%B4%D0%B4%D0%B5%D1%80%D0%B6%D0%B0%D1%82%D1%8C-%D0%B0%D0%B2%D1%82%D0%BE%D1%80%D0%B0-orange.svg?style=flat-square)](https://alexgyver.ru/support_alex/)
[![Foo](https://img.shields.io/badge/README-ENGLISH-blueviolet.svg?style=flat-square)](https://github-com.translate.goog/GyverLibs/pgm_utils?_x_tr_sl=ru&_x_tr_tl=en)  

[![Foo](https://img.shields.io/badge/ПОДПИСАТЬСЯ-НА%20ОБНОВЛЕНИЯ-brightgreen.svg?style=social&logo=telegram&color=blue)](https://t.me/GyverLibs)

# pgm_utils
A set of convenient tools for working with PROGMEM, C++ wrapper for standard pgm functions
- One function to read any data
- Reading multidimensional arrays
- Reading an array of lines

### Compatibility
Compatible with all Arduino platforms (Arduino features are used)

## Contents
- [Use of use](#usage)
- [Versions](#versions)
- [Installation](#install)
- [Bugs and feedback](#feedback)

<a id="usage"></a>

## Use of use
### Macros and functions
```cpp
// synonym for const   FlashStringHelper*
FSTR

// Convert PGM P to FSTR
FPSTR(x)

// Put a single value of val type T in PROGMEM under the name
PGM_VAL(T, name, val)

// place a single value of val type T (class, structure) in PROGMEM under the name, transfer the list for initialization
PGM_STRUCT(T, name, ...)

// Put str in PROGMEM under the name
PGM_STR(name, str)

// place the lines in PROGMEM and in the list of pointers under the name
PGM_STR_LIST(name, ...)
PGM_STR_LIST_STATIC(name, ...)

// put strings in PROGMEM and in the list of pointers + create a StringList object with the name
// will create a progmem array name list and the lines name list 0, ... name list   n
PGM_STR_LIST_OBJ(name, ...)
PGM_STR_LIST_OBJ_STATIC(name, ...)

// Create a pgm::StringList object with the number of rows counted
MAKE_STR_LIST(name)

// Place a Type T Array in PROGMEM under the name
PGM_ARRAY(T, name, ...)

// Place type T arrays in PROGMEM array of pointers under the name
PGM_ARRAY_LIST(T, name, ...)

// create a pgm::Array type T object with a calculated array length
MAKE_ARRAY(T, name)

// Create a PROGMEM array of type T and a pgm class name object:::Array
// Create a progme array name arr
PGM_ARRAY_OBJ(T, name, ...)

// read out
T pgm_read(const T* ptr);
```

### Classes
#### `template <typename T> pgm::Array`
Reading a one-dimensional array

```cpp
Array(const T* arr, size_t len = 0);

// Array length. 0 if not specified at initialization
size_t length();

// index
T operator[](int idx);
```

#### `template <typename T> pgm::ArrayList`
Reading an array of pointers to arrays

```cpp
ArrayList(const T** arr, size_t len = 0);

// Array length. 0 if not specified at initialization
size_t length();

// read the array as pgm::Array by index
Array<T> operator[](int idx);
```

#### `pgm::PString`
Working with PROGEMEM string

```cpp
PString(PGM_P str, size_t len = 0);

// print out
size_t printTo(Print& p);

// line length
size_t length();

// char
void toStr(char* buf);

// pull out
String toString();

// line
bool compare(const char* str);
bool operator==(const char* str);

// line
bool compare(const String& str);
bool operator==(const String& str);

// Get it as FlashStringHelper*
FSTR f_str();

// symbolize
char operator[](int idx);

operator PGM_P();
operator FSTR();
PGM_P pstr;
```

#### `pgm::StringList`
Working with an array of lines from an array of pointers

```cpp
StringList(const char** arr, size_t len = 0);

// Array length. 0 if not specified at initialization
size_t length();

// string
PString operator[](int idx);
```

### Note
`PGM_STR_LIST(name, "str1", "str2", "str3")`unfolds in:
```cpp
const char name_0[] PROGMEM = "str1";
const char name_1[] PROGMEM = "str2";
const char name_2[] PROGMEM = "str3";
const char* const name[] = {name_0, name_1, name_2};
```
> Maximum number of lines -`512`

### Examples
#### Meanings
```cpp
PGM_VAL(int, vali, 123);
PGM_VAL(float, valf, 3.14);

struct Test {
  byte i;
  char str[10];
};
PGM_STRUCT(Test, ptest, 10, "test");

void foo() {
  Serial.println(pgm_read(&vali));  // 123
  Serial.println(pgm_read(&valf));  // 3.14

  Test t = pgm_read(&ptest);
  Serial.println(t.i);    // 10
  Serial.println(t.str);  // test
}
```

#### Lines.
```cpp
PGM_STR(pgmstr, "hello");

void foo() {
  pgm::PString pstr(pgmstr);
  Serial.println(pstr);  //  hello
  Serial.println(pstr.length());  // 5
  for (int i = 0; i < pstr.length(); i++) {
    Serial.print(pstr[i]);
  }
  Serial.println();

  // Use f str() when working with String!
  // It's best.
  String s = pgmstr.f_str();
  s += pgmstr.f_str();
}
```

#### Arrays
```cpp
PGM_ARRAY(byte, pgmarrb, 1, 2, 3);              // pgm
PGM_ARRAY(int, pgmarri, 123, 456, 789);         // pgm
PGM_ARRAY_OBJ(float, arrf, 1.12, 2.34, 3.45);   // array + object pgm::Array

void foo() {
  // length unknown
  pgm::Array<byte> arrb(pgmarrb);
  Serial.println(arrb[1]); // 2
  
  // The length will be counted in Make.
  pgm::Array<int> arri = MAKE_ARRAY(int, pgmarri);
  Serial.println(arri[1]);        // 456
  Serial.println(arri.length());  // 3
 
  // ready-made
  Serial.println(arrf[1]);  // 2.34
}
```

#### Arrays of lines
```cpp
PGM_STR_LIST(pstrlist, "string 1", "kek", "hello");
PGM_STR_LIST_OBJ(pstrlist_obj, "str1", "str2", "str3");

void foo() {
  pgm::StringList list(pstrlist);
  // pgm::StringList list = MAKE STR LIST(pstrlist) The length is known.
  Serial.println(list.length());
  Serial.println(list[1]);
  Serial.println(list[1].length());
  Serial.println(list[0] == "string 1");

  // str1, str2, str3
  for (int i = 0; i < pstrlist_obj.length(); i++) {
    Serial.println(pstrlist_obj[i]);
  }
}
```

<a id="versions"></a>

## Versions
- v1.0

<a id="install"></a>
## Installation
- The library can be found under the name **pgm utils** and installed through the library manager in:
    - Arduino IDE
    - Arduino IDE v2
    - PlatformIO
- [Download the library](https://github.com/GyverLibs/pgm_utils/archive/refs/heads/main.zip).zip archive for manual installation:
    - Unpack and put in *C:\Program Files (x86)\Arduino\libraries* (Windows x64)
    - Unpack and put in *C:\Program Files\Arduino\libraries* (Windows x32)
    - Unpack and put in *Documents/Arduino/libraries/ *
    - (Arduino IDE) Automatic installation from .zip: *Sketch/Connect library/Add .ZIP library...* and specify downloaded archive
- Read more detailed instructions for installing libraries[here](https://alexgyver.ru/arduino-first/#%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0_%D0%B1%D0%B8%D0%B1%D0%BB%D0%B8%D0%BE%D1%82%D0%B5%D0%BA)
### Update
- I recommend always updating the library: new versions fix errors and bugs, as well as optimize and add new features.
- Through the library manager IDE: find the library as when installing and click "Update"
- Manually: **Delete the folder with the old version** and then put the new one in its place. “Replacement” can not be done: sometimes new versions delete files that will remain when replaced and can lead to errors!

<a id="feedback"></a>

## Bugs and feedback
If you find bugs, create **Issue**, or better write to the mail immediately.[alex@alexgyver.ru](mailto:alex@alexgyver.ru)  
The library is open for revision and your **Pull Requests*!

When reporting bugs or incorrect work of the library, it is necessary to specify:
- Library version
- What is used by the IC
- SDK version (for ESP)
- Arduino IDE version
- Are embedded examples that use features and designs that cause bugs in your code working correctly?
- What code was downloaded, what work was expected from it and how it works in reality
- Ideally, attach the minimum code in which the bug is observed. Not a canvas of a thousand lines, but a minimum code.
