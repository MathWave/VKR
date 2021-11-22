from dataclasses import dataclass


@dataclass
class Language:
    id: int
    name: str
    work_name: str
    file_type: str
    logo_url: str
    image: str
    highlight: str

    def __str__(self):
        return self.name


languages = [
    Language(
        id=0,
        name="Python3",
        work_name="Python3",
        file_type="py",
        logo_url="https://entredatos.es/wp-content/uploads/2021/05/1200px-Python-logo-notext.svg.png",
        image="python:3.6",
        highlight="python",
    ),
    Language(
        id=1,
        name="Kotlin",
        work_name="Kotlin",
        file_type="kt",
        logo_url="https://upload.wikimedia.org/wikipedia/commons/0/06/Kotlin_Icon.svg",
        image="zenika/kotlin",
        highlight="kotlin",
    ),
    Language(
        id=2,
        name="C++",
        work_name="Cpp",
        file_type="cpp",
        logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/ISO_C%2B%2B_Logo.svg/1822px-ISO_C%2B%2B_Logo.svg.png",
        image="gcc",
        highlight="cpp",
    ),
    Language(
        id=3,
        name="Java",
        work_name="Java",
        file_type="java",
        logo_url="https://upload.wikimedia.org/wikipedia/ru/thumb/3/39/Java_logo.svg/1200px-Java_logo.svg.png",
        image="openjdk",
        highlight="java"
    ),
    Language(
        id=4,
        name="C#",
        work_name="CSharp",
        file_type="cs",
        logo_url="https://cdn.worldvectorlogo.com/logos/c--4.svg",
        image="mono",
        highlight="csharp"
    )
]
