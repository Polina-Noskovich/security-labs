import React, { useState } from "react";

function App() {
  // Исходный код
  const [sourceCode, setSourceCode] = useState(`
function calculateCircleProperties(radius) {
  return {
    radius: radius,
    diameter: radius * 2,
    circumference: 2 * Math.PI * radius,
    area: Math.PI * Math.pow(radius, 2)
  };
}

function generateRandomNumbers(count, min, max) {
  let numbers = [];
  for (let i = 0; i < count; i++) {
    numbers.push(Math.floor(Math.random() * (max - min + 1)) + min);
  }
  return numbers;
}

const circle = calculateCircleProperties(5);
console.log("Circle properties:", circle);

const randomNumbers = generateRandomNumbers(10, 1, 100);
console.log("Random values:", randomNumbers);
  `);

  const [obfuscatedCode, setObfuscatedCode] = useState("");

  // Обфускация кода
  const obfuscateCode = (code) => {
    function generateRandomString(length) {
      const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
      let result = "";
      for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      return result;
    }

    let varPattern = /([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*[^;]+/g;
    let funcPattern = /function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(/g;
    let paramPattern = /function\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(([^)]*)\)/g;

    let replacements = {};

    code = code.replace(varPattern, (match, p1) => {
      let newName = generateRandomString(6);
      replacements[p1] = newName;
      return match.replace(p1, newName);
    });

    code = code.replace(funcPattern, (match, p1) => {
      let newName = generateRandomString(6);
      replacements[p1] = newName;
      return match.replace(p1, newName);
    });

    code = code.replace(paramPattern, (match, p1) => {
      let params = p1.split(",").map((param) => param.trim()).filter((param) => param);
      let newParams = params.map((param) => {
        let newName = generateRandomString(6);
        replacements[param] = newName;
        return newName;
      });
      return match.replace(p1, newParams.join(","));
    });

    for (let oldName in replacements) {
      let newName = replacements[oldName];
      let regEx = new RegExp(`\\b${oldName}\\b`, "g");
      code = code.replace(regEx, newName);
    }

    let lines = code.split("\n");
    lines = lines.filter((line) => line.trim() !== "");

    let obfuscatedCode = lines.join(" ");

    obfuscatedCode = obfuscatedCode
      .replace(/\s*([+\-*/=<>!&|(){}[\],;.])\s*/g, "$1")
      .replace(/\s{2,}/g, " ")
      .replace(/; /g, ";")
      .replace(/ ,/g, ",")
      .replace(/ \)/g, ")")
      .replace(/ \{/g, "{")
      .replace(/ \}/g, "}");

    return obfuscatedCode;
  };

  // Обработчик обфускации
  const handleObfuscate = () => {
    const result = obfuscateCode(sourceCode);
    setObfuscatedCode(result);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">Обфускация кода</h1>
      <p className="text-gray-700 mb-4 max-w-2xl text-center">
        Обфускация кода — это процесс преобразования исходного кода в менее читаемый вид, чтобы усложнить его анализ.
        Здесь вы можете вставить JavaScript-код, обфусцировать его и увидеть результат.
      </p>
      <div className="flex flex-col md:flex-row gap-4 w-full max-w-4xl">
        <div className="flex-1">
          <h2 className="text-lg font-semibold mb-2">Исходный код:</h2>
          <textarea
            className="w-full h-60 p-3 border border-gray-300 rounded-md"
            value={sourceCode}
            onChange={(e) => setSourceCode(e.target.value)}
          ></textarea>
        </div>
        <div className="flex-1">
          <h2 className="text-lg font-semibold mb-2">Обфусцированный код:</h2>
          <textarea
            className="w-full h-60 p-3 border border-gray-300 rounded-md bg-gray-200"
            value={obfuscatedCode}
            readOnly
          ></textarea>
        </div>
      </div>
      <button
        onClick={handleObfuscate}
        className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
      >
        Обфусцировать код
      </button>
      <div className="mt-8 max-w-3xl text-gray-700">
        <h3 className="text-lg font-semibold mb-2">Как работает обфускация:</h3>
        <p className="mb-2">
          Обфускация заменяет имена функций, переменных и параметров на случайные строки. Это делает код менее читаемым,
          но он продолжает выполнять ту же функцию. Например:
        </p>
        <ul className="list-disc list-inside mb-4">
          <li>Переменные <code>radius</code> могут стать <code>AbCdEf</code>.</li>
          <li>Функции <code>calculateCircleProperties</code> могут стать <code>XyZ123</code>.</li>
        </ul>
        <p>
          Такой процесс полезен для защиты интеллектуальной собственности, но его следует использовать с осторожностью.
        </p>
      </div>
    </div>
  );
}

export default App;