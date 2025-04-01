import React, { useState } from "react";
import { Dialog } from "@headlessui/react";
import { XCircle } from "lucide-react";

function App() {

  const [sourceCode, setSourceCode] = useState(`function calculate(a, b) {
  const sum = a + b;
  const product = a * b;
  return {
    sum: sum,
    product: product,
    difference: Math.abs(a - b)
  };
}
  `);

  const [isModalOpen, setIsModalOpen] = useState(false);


  const [obfuscatedCode, setObfuscatedCode] = useState("");

  const obfuscateCode = (code) => {
    function generateRandomString(length) {
      const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890АИВГДабвгд";
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
      let newName = generateRandomString(10);
      replacements[p1] = newName;
      return match.replace(p1, newName);
    });

    code = code.replace(funcPattern, (match, p1) => {
      let newName = generateRandomString(10);
      replacements[p1] = newName;
      return match.replace(p1, newName);
    });

    code = code.replace(paramPattern, (match, p1) => {
      let params = p1.split(",").map((param) => param.trim()).filter((param) => param);
      let newParams = params.map((param) => {
        let newName = generateRandomString(10);
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

  const handleObfuscate = () => {
    const result = obfuscateCode(sourceCode);
    setObfuscatedCode(result);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">Лабораторная №7. Обфускация кода</h1>
      <hr className="border-gray-500 my-4 w-full max-w-3xl" />
      <p className="text-gray-700 mb-4 max-w-2xl text-center">
        Обфускация кода — это процесс преобразования исходного кода в менее читаемый вид, чтобы усложнить его анализ.
        Здесь вы можете вставить JavaScript-код, обфусцировать его и увидеть результат.
      </p>
      <hr className="border-gray-500 my-4 w-full max-w-3xl" />
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
  className="mt-4 px-6 py-2 text-white rounded-md bg-gradient-to-r from-gray-900 via-gray-600 to-gray-900 hover:from-gray-600 hover:via-gray-900 hover:to-gray-600 transition-all shadow-lg"
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
          <li>Переменные <code>product</code> могут стать <code>YueГXваxsR</code>.</li>
          <li>Функции <code>calculate(a, b)</code> могут стать <code>KO9MuPMpMW(P9RB8fUqBt,9дPZ8OCPbt)</code>.</li>
        </ul>
        <p>
          Такой процесс полезен для защиты интеллектуальной собственности, но его следует использовать с осторожностью.
        </p>
        <hr className="border-gray-500 my-4 w-full max-w-3xl" />
        <p
          onClick={() => setIsModalOpen(true)}
          className="text-center text-2xl text-gray-800 cursor-pointer hover:text-red-600 transition"
        >
          С 1 апреля :)
        </p>
      </div>

      <Dialog open={isModalOpen} onClose={() => setIsModalOpen(false)} className="relative z-50">
        <div className="fixed inset-0 bg-black/40" aria-hidden="true" />
        <div className="fixed inset-0 flex items-center justify-center p-4">
          <Dialog.Panel className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl text-center">
            <XCircle className="mx-auto h-12 w-12 text-red-500 mb-4" />
            <Dialog.Title className="text-xl font-bold text-gray-800">
              404
            </Dialog.Title>
            <p className="mt-2 text-gray-600">
              У вас белая спина
            </p>
            <button
              onClick={() => setIsModalOpen(false)}
              className="mt-6 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
            >
              Закрыть
            </button>
          </Dialog.Panel>
        </div>
      </Dialog>
    </div>
  );
}

export default App;