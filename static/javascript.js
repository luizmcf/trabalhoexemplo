function meu_callback_origem(conteudo) {
    if (!("erro" in conteudo)) {
        //Atualiza os campos com os valores.
        document.getElementById('rua_ori').value=(conteudo.logradouro);
        document.getElementById('num_ori').value="";
        document.getElementById('bairro_ori').value=(conteudo.bairro);
        document.getElementById('cidade_ori').value=(conteudo.localidade);
        document.getElementById('uf_ori').value=(conteudo.uf);
    }
    else {
        //CEP não Encontrado.
        alert("CEP não encontrado.");
    }
}
    
function pesquisacep_origem(valor) {
    //Nova variável "cep" somente com dígitos.
    var cep = valor.replace(/\D/g, '');

    //Verifica se campo cep possui valor informado.
    if (cep != "") {

        //Expressão regular para validar o CEP.
        var validacep = /^[0-9]{8}$/;

        //Valida o formato do CEP.
        if(validacep.test(cep)) {

            //Preenche os campos com "..." enquanto consulta webservice.
            document.getElementById('rua_ori').value="...";
            document.getElementById('num_ori').value="...";
            document.getElementById('bairro_ori').value="...";
            document.getElementById('cidade_ori').value="...";
            document.getElementById('uf_ori').value="...";

            //Cria um elemento javascript.
            var script = document.createElement('script');

            //Sincroniza com o callback.
            script.src = 'https://viacep.com.br/ws/'+ cep + '/json/?callback=meu_callback_origem';

            //Insere script no documento e carrega o conteúdo.
            document.body.appendChild(script);

        }
        else {
            //cep é inválido.
            alert("Formato de CEP inválido.");
        }
    } 
}

function meu_callback_destino(conteudo) {
    if (!("erro" in conteudo)) {
        //Atualiza os campos com os valores.
        document.getElementById('rua_des').value=(conteudo.logradouro);
        document.getElementById('num_des').value="";
        document.getElementById('bairro_des').value=(conteudo.bairro);
        document.getElementById('cidade_des').value=(conteudo.localidade);
        document.getElementById('uf_des').value=(conteudo.uf);
    }
    else {
        //CEP não Encontrado.
        alert("CEP não encontrado.");
    }
}
    
function pesquisacep_destino(valor) {
    //Nova variável "cep" somente com dígitos.
    var cep = valor.replace(/\D/g, '');

    //Verifica se campo cep possui valor informado.
    if (cep != "") {

        //Expressão regular para validar o CEP.
        var validacep = /^[0-9]{8}$/;

        //Valida o formato do CEP.
        if(validacep.test(cep)) {

            //Preenche os campos com "..." enquanto consulta webservice.
            document.getElementById('rua_des').value="...";
            document.getElementById('num_des').value="...";
            document.getElementById('bairro_des').value="...";
            document.getElementById('cidade_des').value="...";
            document.getElementById('uf_des').value="...";

            //Cria um elemento javascript.
            var script = document.createElement('script');

            //Sincroniza com o callback.
            script.src = 'https://viacep.com.br/ws/'+ cep + '/json/?callback=meu_callback_destino';

            //Insere script no documento e carrega o conteúdo.
            document.body.appendChild(script);

        }
        else {
            //cep é inválido.
            alert("Formato de CEP inválido.");
        }
    } 
};