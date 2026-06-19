---
applyTo: "**/*.cpp,**/*.hpp"
---


# C++ formatting rules for Copilot code review

Do not review code to follow formatting rules. That is the CI's job.
When suggesting C++ code changes, follow these formatting rules.

## Format rules

clang-format
```
---
Language: Cpp
BasedOnStyle: Google

AccessModifierOffset: -2
AlignAfterOpenBracket: AlwaysBreak
BraceWrapping:
  AfterClass: true
  AfterFunction: true
  AfterNamespace: true
  AfterStruct: true
  AfterEnum: true
BreakBeforeBraces: Custom
ColumnLimit: 120
ConstructorInitializerIndentWidth: 0
ContinuationIndentWidth: 2
DerivePointerAlignment: false
PointerAlignment: Middle
ReflowComments: false
...
```
