import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
  const filePath = path.resolve('public', 'codes.txt');


  try {
    let codes = fs.readFileSync(filePath, 'utf-8')
      .split('\n')
      .map(c => c.trim())
      .filter(Boolean);

    if (codes.length === 0) {
      res.status(404).json({ error: 'Промокоды закончились' });
      return;
    }

    const selected = codes[0];
    const remaining = codes.slice(1);

    fs.writeFileSync(filePath, remaining.join('\n'));

    res.status(200).json({ code: selected });
  } catch (e) {
    res.status(500).json({ error: 'Ошибка сервера при выдаче кода' });
  }
}

