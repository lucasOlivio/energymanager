$(function() {
	function loading(type) {
		if(type=='open'){
			$("#loader").show();
			$("#myDiv").hide();
		}else{
			$("#loader").hide();
			$("#myDiv").show();
		}
	}

	function random_rgba() {
	    var o = Math.round, rand = Math.random, s = 255;
	    var r = o(rand()*s), g = o(rand()*s), b = o(rand()*s);
	    for (; (r+g+b < 240 || r+g+b > 400);) {
	    	r = o(rand()*s); g = o(rand()*s); b = o(rand()*s);
    }
	    return 'rgba(' + r + ',' + g + ',' + b + ', 0.2)';
	}

	function daysInMonth (month, year) {
	    return new Date(year, month, 0).getDate();
	}

	$('#buscarTb').on('click',function(e){
		e.preventDefault();
		loading('open');
		var env = {};
		env.mes = $('#mes').val();
		env.ano = $('#ano').val();
		var tensao = parseFloat($('#tensao').val());
		$.ajax({
			url: '/tbData',
			data: env,
			type: 'POST',
			dataType: 'json',
			success: function(data){
				var linhas = '';
				var color = '';
				var icon = '<i class="fas fa-minus"></i>';
				var pct = 0;
				var ATotal = 0;
				var pctHj = 0;
				var kw1 = 0;
				var kw2 = 0;
				var dif = 0;
				var div = 0;
				$('#tbodyDetalhes').html('');
				$.each(data.tabela, function(key, val){
					ATotal += val[2];
					pct = parseFloat(((val[3]/data.total)*100)).toFixed(2);
					if(isNaN(pct)){
						pct=0;
					}
					if(val[2]==null || val[2]==0){
						val[2]==1;
					}
					if(val[3]==null){
						val[3]=0;
					}
					dif = val[2]-val[3];
					div = val[3];
					if(div==0){
						div=1;
					}
					pctHj = parseFloat(((dif/div)*100)).toFixed(2);
					if(pctHj>0){
						icon = '<i class="fas fa-sort-up text-danger"></i>';
						color = 'class="text-danger"';
					}else if(pctHj<0){
						icon = '<i class="fas fa-sort-down text-success"></i>';
						color = 'class="text-success"';
					}
					kw1 = ((val[3]*tensao)/1000).toFixed(2);
					linhas += '<tr>';
					linhas += '<td>'+val[0]+'</td>\
								<td>'+val[1]+'</td>\
								<td>'+val[3]+' A</td>\
								<td>'+kw1+' KWh</td>\
								<td '+color+'>'+pctHj+'% '+icon+'</td>\
								<td>'+pct+'%</td>';
					linhas += '</tr>';
				});
				if(data.total==null){
					data.total=0;
				}
				kw1 = ((data.total*tensao)/1000).toFixed(2);
				dif = ATotal-data.total;
				div = data.total;
				if(div==0){
					div=1;
				}
				pctHj = parseFloat(((dif/div)*100)).toFixed(2);
				if(pctHj>0){
					icon = '<i class="fas fa-sort-up text-danger"></i>';
					color = 'class="text-danger"';
				}else if(pctHj<0){
					icon = '<i class="fas fa-sort-down text-success"></i>';
					color = 'class="text-success"';
				}
				$('#tbodyDetalhes').html('<tr class="table-info">\
											<td>\
												<i class="fas fa-globe"></i>\
											</td>\
											<td>\
												Total\
											</td>\
											<td>\
												'+data.total+' A\
											</td>\
											<td>\
												'+kw1+' KWh\
											</td>\
											<td '+color+'>\
												'+pctHj+' % '+icon+'</i>\
											</td>\
											<td>\
												100%\
											</td>\
										</tr>');
				$('#tbodyDetalhes').append(linhas);
				loading('close');
			},
			error: function(data){
				console.log(data)
			}
		});
	});

	function graph(){
		loading('open');
		var env = {};
		env.de = $('#de').val();
		env.ate = $('#ate').val();
		env.freq = $('#frequencia').val();
		env.tensao = $('#tensaoGraph').val();
		$.ajax({
			url: '/graph',
			data: env,
			type: 'POST',
			dataType: 'json',
			success: function(retorno){
				var ctx = document.getElementById("canvas").getContext("2d");
				var labels = [];
				var i = 0;
				var index = 0;
				var data = [];
				var cor = '';
				$.each(retorno.rp.labels,function(key,val){
					labels.push(val[0]);
				});
				var datasets = [];
				$.each(retorno.rp.locais, function(key,val){
					data = [];
					i=0;
					cor = '';
					$.each(val, function(k,v){
						index = labels.indexOf(v[1]);
						if(index>-1){
							if(i<index){
								for (var x = i; i <= index-1; i++) {
									data.push(0);
								}
							}
							data.push(v[0]);
							i++;
						}else{
							for (var x = i; i <= index; i++) {
								data.push(0);
							}
						}
					});
					cor = random_rgba();
					datasets.push({
							    		label: key,
							    		data: data,
							    		backgroundColor: [cor],
							            borderColor: [cor.replace('0.2','1')],
							            borderWidth: 1
							    	});
				});
				window.myLineChart = new Chart(ctx, {
				    type: 'line',
				    data: {
				    	labels: labels,
				    	datasets: datasets
				    },
				    options: {
				        elements: {
				            line: {
				                tension: 0.2, // disables bezier curves
				            },
				            point:{
				            	radius: 1
				            }
				        }
				    }
				});
				loading('close');
			},
			error: function(data){
				console.log(data)
			}
		});
	}

	function listaLocais(){
		$.ajax({
			url: '/cad',
			data: {acao:'lista'},
			type: 'POST',
			dataType: 'json',
			success: function(data){
				var color = '';
				var stt = '';
				var linhas = '';
				$.each(data.rp,function(key,val){
					if(val[3]){
						color = 'table-success';
						stt = 'Ativo';
					}else{
						color = 'table-danger';
						stt = 'Inativo';
					}
					linhas += '<tr stt='+stt+' class="'+color+'">';
					$.each(val, function(k,v){
						if(k!=3){
							linhas += '<td>'+v+'</td>';
						}else{
							linhas += '<td>'+stt+'</td>';
						}
					});
					linhas += '</tr>';
				});
				$('#tbodyCad').html(linhas);
				loading('close');
			},
			error: function(data){
				console.log(data)
			}
		});
	}

	$(document).on('click','#buscarGraph',function(){
		myLineChart.destroy();
		graph();
	});

	$(document).on('click','#tbodyCad tr', function(){
		$('#tbodyCad tr.table-info').removeClass('table-info');
		$(this).addClass('table-info');
		$('#idLocal').val($(this).find('td:eq(0)').html());
		$('#local').val($(this).find('td:eq(2)').html());
		M.updateTextFields();
	});

	$(document).on('click','#salvar',function(){
		if($('#idLocal').val()!=''){
			loading('open');
			var env = {};
			env.acao = 'salvar';
			env.id = $('#idLocal').val();
			env.local = $('#local').val();
			$.ajax({
				url: '/cad',
				data: env,
				type: 'POST',
				dataType: 'json',
				success: function(data){
					if(data.rp>0){
						var toastHTML = '<span>Atualizado com sucesso!</span>';
			  			M.toast({
			  				html: toastHTML,
			  				classes: 'bg-success'
			  			});
					}else{
						var toastHTML = '<span>Nenhum local encontrado!</span>';
			  			M.toast({
			  				html: toastHTML,
			  				classes: 'bg-info'
			  			});
					}
					listaLocais();
					loading('close');
				},
				error: function(data){
					console.log(data)
				}
			});
		}else{
			var toastHTML = '<span>Nenhum local selecionado!</span>';
  			M.toast({
  				html: toastHTML,
  				classes: 'bg-danger'
  			});
		}
	});

	$(document).on('click','#io',function(){
		if($('#idLocal').val()!=''){
			loading('open');
			var env = {};
			env.acao = 'io';
			env.status = $('#tbodyCad tr.table-info').attr('stt');
			env.id = $('#idLocal').val();
			$.ajax({
				url: '/cad',
				data: env,
				type: 'POST',
				dataType: 'json',
				success: function(data){
					if(data.rp>0){
						var toastHTML = '<span>Local alterado com sucesso!</span>';
			  			M.toast({
			  				html: toastHTML,
			  				classes: 'bg-success'
			  			});
					}else{
						var toastHTML = '<span>Nenhum local encontrado!</span>';
			  			M.toast({
			  				html: toastHTML,
			  				classes: 'bg-info'
			  			});
					}
					listaLocais();
					loading('close');
				},
				error: function(data){
					console.log(data)
				}
			});
		}else{
			var toastHTML = '<span>Nenhum local selecionado!</span>';
  			M.toast({
  				html: toastHTML,
  				classes: 'bg-danger'
  			});
		}
	});

	$('#buscarTb').trigger('click');
	$('.calendario').mask('00/00/0000');
	var today = new Date();
	var m = today.getMonth()+1; //January is 0!
	if(m<10){
		m = '0'+m;
	}
	var y = today.getFullYear();
	$('#de').val('01/'+m+'/'+y);
	$('#ate').val(daysInMonth(m,y)+'/'+m+'/'+y);
	$(".calendario").datepicker({
	    dateFormat: 'dd/mm/yy',
	    dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
	    dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
	    dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
	    monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
	    monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
	    nextText: 'Próximo',
	    prevText: 'Anterior'
	});
	graph();
	listaLocais();
});