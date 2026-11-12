# Sua missão

Encontre a saída **S**. Você é **@**; os tesouros são **\***.
Cada partida gera um labirinto novo. Tesouros são opcionais.

## Controles
- **W / seta para cima**: subir
- **S / seta para baixo**: descer
- **A / seta para esquerda**: esquerda
- **D / seta para direita**: direita
- **Q / Esc**: abandonar a partida

Mantenha o foco no terminal enquanto joga. Não é necessário apertar Enter.
No modo `--teclado linha`, digite WASD ou Q e confirme com Enter.

## Pontos e fim da partida
Você começa com 100 pontos. Cada passo válido custa 1 ponto; bater na
parede custa 2. Cada tesouro vale 25 e alcançar a saída rende 100 pontos.
A pontuação mínima é zero. Atingir zero não encerra o jogo.
Você perde ao abandonar ou esgotar o limite de movimentos válidos.
Chegar à saída no último movimento permitido ainda conta como vitória.

## Solução automática
A opção 3 do menu mostra uma busca recursiva até a saída.
Ela usa as mesmas regras e limite do modo manual, sem buscar todos os tesouros.
Use `--seed 42` para repetir o mesmo mapa e `--demo` para assistir diretamente.
