module.exports = {
    // Globale regels
    rules: {
      // Voorbeelden van regels
      'no-console': 'error', // Verbiedt het gebruik van console.log
      'semi': ['error', 'always'], // Vereist puntkomma's aan het einde van regels
      'indent': ['error', 2], // Indentatie met 2 spaties
    },
  
    // Omgeving specifieke regels
    env: {
      // Voorbeelden van omgevingen
      node: true, // Schakelt regels in die relevant zijn voor Node.js
      es6: true, // Schakelt regels in die relevant zijn voor ES6
    },
  
    // Extends
    extends: [
      // Voorbeelden van extends
      'eslint:recommended', // Gebruikt de aanbevolen regels van ESLint
      'plugin:react/recommended', // Gebruikt de aanbevolen regels voor React
    ],
  
    // Plugins
    plugins: [
      // Voorbeelden van plugins
      'react', // Maakt het mogelijk om regels te gebruiken die specifiek zijn voor React
      // 'plugin:prettier', // Integreert ESLint met Prettier
    ],
  };
  