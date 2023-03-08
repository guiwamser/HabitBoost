var api_url = 'http://localhost:8000/api/v1/usuarios';

// ela realiza uma busca de aluno por id e retorna professor Json
function get_by_id(id_usuario){
    let usuario = fetch(`${api_url}/${id_usuario}`)
    .then(response => response.text())
    .then(function(text) {    
        return JSON.parse(text);
    });   
    return usuario;
 }
 
 
function load_usuario(id_usuario){
    get_by_id(id_usuario).then(usuario =>{
        document.getElementById("id").value = usuario.id;
        document.getElementById("nome").value = usuario.nome;
        document.getElementById("email").value = usuario.email;
        document.getElementById("senha").value = usuario.senha
    });
  
}
 
//Botao salvar tanto para criar quanto editar
function save(){
    let nome = document.getElementById("nome").value;
    let email = document.getElementById("email").value;
    let senha = document.getElementById("senha").value;

    if (id !== null && id !== '' && id !== 0) {
        console.log('editar')
        usuario = {"id":id, "nome": nome, "email": email, "senha": senha}
        update(usuario);
    } else {
        usuario = {"nome": nome, "email": email, "senha": senha}
        create(usuario);
    }
}

 
 
function update(usuario){
    let mensagem = document.getElementById("mensagem");
    fetch(`${api_url}/${usuario.id}`,{
        method: 'PUT',
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(usuario)
    })

    .then(response => {
        if(response.status == 202){
            mensagem.innerHTML = "Alterado com sucesso";
        }else{
            mensagem.innerHTML = "Erro";
        }
    })
}
 
 
function create(usuario){
    let mensagem = document.getElementById("mensagem");
    fetch(api_url,{
        method: 'POST',
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(usuario)
    })
    .then(response => {
        console.log(response); // Loga a resposta do servidor na console
        if(response.status == 201){
            alert = "Usuário criado com sucesso";
            window.location.href = "login.html"; // redireciona para a página lista.html
        }else{
            mensagem.innerHTML = "Erro";
        }
    })
}
 
function remove(id){
    fetch(`${api_url}/${id}`,{
        method: 'DELETE',
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => {
        if(response.status == 204){
            get_all();
        }else{
            alert("Erro");
        }
    })
}

function login(event) {
    event.preventDefault(); // Evita que a página seja recarregada após enviar o formulário
  
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
  
    fetch(`${api_url}?email=${email}`)    
      .then(response => response.json())
      .then(data => {
        if (data.length > 0 && data[0].senha === senha) {
          // Login correto, redirecionar para dia.html
          window.location.href = "dia.html";
        } else {
          alert('Email ou senha incorretos');
        }
      })
      .catch(error => console.error(error));
  }
  
  const loginForm = document.getElementById('login-form');
  loginForm.addEventListener('submit', login);
  
