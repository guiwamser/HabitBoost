var api_url = 'http://localhost:8000/api/v1/habitos';

//funcao para pegar todos
function get_all(){
    //Fetch metodo JavaScript para acessar e manipular HTTP, tais como os pedidos e respostas. 
    fetch(api_url)
    
    .then(response =>response.text())
    .then(function(text) {
        //variavel body acessando o documento, html manipulando tag tbodyusuarios
        let tbody = document.getElementById('tbody-habitos');
        //variavel let dados convertendo text para json
        let dados = JSON.parse(text);
        //tbody innerHtml recebe uma lista vazia
        tbody.innerHTML = '';

        //variavel dados que recebe o nosso texte entra em um foreach
        //criamos variavel de habito
        dados.forEach(habito => {
        //tbody inner html incrementando dados convertidos para incrementar nos hmtl
        tbody.innerHTML += ` <tr>
            <td>${habito.hora}</td>
            <td>${habito.descricao}</td>
            <td>
                <a href="usuariosave.html?id=${habito.id}">editar</a> |
                <button onclick='remove(${habito.id})'>deletar</button>
            </td>
        </tr>
        `;
      });
    })
}

//Buscar por usuario
function search(){
    //variavel id aluno acessando documento html acessando campo idbuscae seu valor
    let id_habito = document.getElementById('id-busca').value;
    //imprimindo id_aluno
    console.log(id_habito)
    // se id aluno for diferente de vazio
    if(id_habito != ''){
        //acesse api url da nossa string
        api_url = `${api_url}/${id_habito}`
    }
    else{
        return;
    }
 
 
    fetch(api_url)
    .then(response => response.text())
    .then(function(text) {
      let tbody = document.getElementById('tbody-habitos');     
      let habito = JSON.parse(text);
      console.log(habito);    
      
      tbody.innerHTML = ` <tr>
        <td>${habito.id}</td>
        <td>${habito.descricao}</td>
        <td>${habito.dia_semana}</td>
        <td>${habito.hora}</td>
        <td>
            <a href="usuariosave.html?id=${habito.id}">editar</a> |
            <button onclick='remove(${habito.id})'>deletar</button>
        </td>
      </tr>`;
    });
 }

// ela realiza uma busca de aluno por id e retorna professor Json
function get_by_id(id_habito){
    let usuario = fetch(`${api_url}/${id_habito}`)
    .then(response => response.text())
    .then(function(text) {    
        return JSON.parse(text);
    });   
    return habito;
 }
 
 
function load_usuario(id_habito){
    get_by_id(id_habito).then(habito =>{
        document.getElementById("id").value = usuario.id;
        document.getElementById("descricao").value = usuario.descricao;
        document.getElementById("dia_semana").value = usuario.dia_semana;
        document.getElementById("hora").value = usuario.hora;
    });
  
}
 
//Botao salvar tanto para criar quanto editar
function save(){
    let id = document.getElementById("id").value;
    let descricao = document.getElementById("descricao").value;
    let dia_semana = document.getElementById("dia_semana").value;
    let hora = document.getElementById("hora").value;
       
    if(id != ''){
        console.log('editar')
        usuario = {"id":id, "descricao": descricao, "dia_semana": dia_semana, "hora": hora}
        update(habito);
    }
    else{
        usuario = {"descricao": descricao, "dia_semana": dia_semana, "hora": hora}
        create(habito);
    }       
}
 
 
function update(habito){
    let mensagem = document.getElementById("mensagem");
    fetch(`${api_url}/${habito.id}`,{
        method: 'PUT',
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(habito)
    })

    .then(response => {
        if(response.status == 202){
            mensagem.innerHTML = "Alterado com sucesso";
        }else{
            mensagem.innerHTML = "Erro";
        }
    })
}
 
 
function create(habito){
    let mensagem = document.getElementById("mensagem");
    fetch(api_url,{
        method: 'POST',
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(habito)
    })
    .then(response => {
        if(response.status == 201){
         
            mensagem.innerHTML = "Criado com sucesso";
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

function get_all() {
    fetch('/habitos')
      .then(response => response.json())
      .then(function(data) {
        let tbody = document.getElementById('tbody-habitos');
        tbody.innerHTML = '';
  
        data.forEach(habito => {
          tbody.innerHTML += ` <tr>
            <td>${habito.hora}</td>
            <td>${habito.descricao}</td>
            <td>
              <a href="habitosave.html?id=${habito.id}">editar</a> |
              <button onclick='remove(${habito.id})'>deletar</button>
            </td>
          </tr>
          `;
        });
      });
  }
  