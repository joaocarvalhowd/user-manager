# Gerenciador de usuários

CAP 2 - ENTRANDO NO MUNDO DOS RÉPTEIS - DESENVOLVER UMA FERRAMENTA PARA GERENCIAMENTO DE USUÁRIO

# Instalar projeto

```sh
pip install -r requirements.txt
```

**Alunos:** [João Victor Barbosa de Carvalho](https://github.com/joaocarvalhowd), [Marco Luiz Gonzaga](https://github.com/pixelcake), [Bruno Caoe Ferreira Spera](https://github.com/brunospera)

### Desenvolver uma ferramenta para gerenciar usuários. 

#### Você deverá armazenar os seguintes dados de cada usuário: 
    * nome completo, 
    * nome reduzido (como é chamado dentro do ambiente de trabalho – não poderão existir dois usuários com nomes reduzidos iguais), 
    * cargo, nível de acesso (o nível de acesso será dividido em: visitante, usuário, administrativo, técnico e super-usuário), 
    * data e hora do último acesso (considere os dois dados como string).

#### Além disso
 - [x] cadastrar usuários em uma lista; 
 - [x] retornar quantos super-usuários existem armazenados na lista; 
 - [x] excluir um usuário através do nome reduzido; 
 - [x] pesquisar usuário pelo nome reduzido; 
 - [x] retornar todos os usuários de acordo com o nível de acesso. 
 - [x] retornar os usuários que tiveram acesso o último acesso através de uma data especificada.

Por esse ser um projeto acadêmico alguns pontos não funcionarão como num projeto real, de qualquer forma fizemos o máximo para gerar uma usabilidade agradável, e para esse projeto utilizamos o microfrawork Flask Python (http://flask.pocoo.org/docs/1.0/) para realização do trabalho.
Para gerar a data de acesso o usuário deverá fazer o login, foi utilizada a tag Date que dispara um calendário em navegadores modernos exceto o Safari que converte o mesmo em Text. Poderia ser implementado um JS para corrigir isso e tornar Cross Browser.
Num sistema ideal somente um super-user deveria ter acesso ao cadastro e outras funções, no caso desse trabalho qualquer um com acesso pode cadastrar, editar e excluir.
Foi implementado CSS que estava fora do escopo do porjeto para que o mesmo ficasse mais agradável.

###### Algumas imagens das telas do projeto:
![Login page](https://pentest.tools/fiap/img/login.jpg)
---
![Main page](https://pentest.tools/fiap/img/main-page.jpg)
---
![Insert user page](https://pentest.tools/fiap/img/insert-user.jpg)
---
![Edit user page](https://pentest.tools/fiap/img/edit-user.jpg)
---
![Filter by access level](https://pentest.tools/fiap/img/filter-user-by-level-access.jpg)
