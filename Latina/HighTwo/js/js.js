var current_card = [];
var big_blind = 10;
var small_blind = 5;
var decide_blind = random_number(2); // 偶數代表AI小盲，奇數代表玩家小盲
var my_check = false;
var enemy_check = false;
var point_player;
var next_step;
var turn_number; //當前回合數
var turn_log = [];
var enemy_card_level; //敵人手牌 牌力


function init_game(){
	turn_number = 0; //初始化回合數為1
	enemy_card_level = 0;

	//將電腦的牌蓋回去
	$(".game_table_content > div > .card_wrap[card_type=" + 'enemy_card1' + "]").removeClass('active');
	$(".game_table_content > div > .card_wrap[card_type=" + 'enemy_card2' + "]").removeClass('active');

	//下面將牌隱藏歸位
	var all_card_type = ["enemy_card1","enemy_card2","my_card1","my_card2","public_card1","public_card2","public_card3","public_card4","public_card5"];
	all_card_type.forEach(function(value,index){
		$(".game_table_content > div > .card_wrap[card_type=" + value + "]").addClass('card_transparent');
	});

	//決定大盲小盲，並更改初始賭資
	if(decide_blind % 2 == 0){
		var my_chip = $(".my_chip .my_chip_value span").html(big_blind);
		var enemy_chip = $(".enemy_chip .enemy_chip_value span").html(small_blind);
		point_player = 'enemy';
		turn_log = [0, 1, small_blind, 1, 0, big_blind];
	}
	else{
		var my_chip = $(".my_chip .my_chip_value span").html(small_blind);
		var enemy_chip = $(".enemy_chip .enemy_chip_value span").html(big_blind);
		point_player = 'my';
		turn_log = [0, 0, small_blind, 1, 1, big_blind];
	}

	//ㄙㄟ掰ˊ
	shuffle_card();
	
	//把洗好的設定進牌裡面
	all_card_type.forEach(function(value,index){
		$(".game_table_content > div > .card_wrap[card_type=" + value + "]").attr('card_number',current_card[index]);
	});

	//發牌
	setTimeout(function(){
		give_card_step1();
	}, 637);

	
	setTimeout(function(){	//檢查回合
		check_turn();
	}, 2000);
}


//----------------------------------------

function random_number(num){
	return Math.floor(Math.random()*num);
}

function init_card(){
	for(var i=1;i<=52;i++){
		current_card.push(i);
	}
}

function shuffle_card(){
	var new_card = [];
	for(var i=current_card.length;i>0;i--){
		var random = random_number(i);
		new_card.push(current_card[random]);
		current_card.splice(random,1);
	}

	current_card = new_card;

	/*
	//我要作弊區! 指定牌型!
	current_card[0] = 1; //A2
	current_card[1] = 5; //A3
	current_card[2] = 3; //C2
	current_card[3] = 26; //B8
	current_card[4] = 49; //A1
	current_card[5] = 25; //A8
	current_card[6] = 51; //C1
	current_card[7] = 10; //B4
	current_card[8] = 13; //A5
	*/
}

function give_card_step1(){
	var next_card_type = ["enemy_card1","enemy_card2","my_card1","my_card2"];

	next_card_type.forEach(function(value,index){
		var stack_card_top = $(".card_stack .card_wrap.card_stack_position").offset().top;
		var stack_card_left = $(".card_stack .card_wrap.card_stack_position").offset().left;
		var hand_card_top = $(".game_table_content > div > .card_wrap[card_type=" + value + "]").offset().top;
		var hand_card_left = $(".game_table_content > div > .card_wrap[card_type=" + value + "]").offset().left;

		//將牌發到指定位置
		$(".card_stack .card_wrap[card_type=" + value + "]").css("top",hand_card_top - stack_card_top + "px");
		$(".card_stack .card_wrap[card_type=" + value + "]").css("left",hand_card_left - stack_card_left + "px");

		setTimeout(function(){
			//顯示出真正的牌
			$(".game_table_content > div > .card_wrap[card_type=" + value + "]").removeClass('card_transparent');

			//把假牌歸位
			$(".card_stack .card_wrap[card_type=" + value + "]").css('display','none'); //把牌隱藏
			$(".card_stack .card_wrap[card_type=" + value + "]").css("top",0 + "px");
			$(".card_stack .card_wrap[card_type=" + value + "]").css("left",0 + "px");
		}, 1000);

		setTimeout(function(){
			$(".card_stack .card_wrap[card_type=" + value + "]").css('display','block'); //把牌顯示
		}, 2000);
	});
	check_card_background(); //顯示牌的花色號碼
	next_step = 'step2';
	my_check = false;
	enemy_check = false;
}

function give_card_step2(){
	var next_card_type = ["public_card1","public_card2","public_card3"];

	next_card_type.forEach(function(value,index){
		var stack_card_top = $(".card_stack .card_wrap.card_stack_position").offset().top;
		var stack_card_left = $(".card_stack .card_wrap.card_stack_position").offset().left;
		var hand_card_top = $(".game_table_content > div > .card_wrap[card_type=" + value + "]").offset().top;
		var hand_card_left = $(".game_table_content > div > .card_wrap[card_type=" + value + "]").offset().left;

		//將牌發到指定位置
		$(".card_stack .card_wrap[card_type=" + value + "]").css("top",hand_card_top - stack_card_top + "px");
		$(".card_stack .card_wrap[card_type=" + value + "]").css("left",hand_card_left - stack_card_left + "px");

		setTimeout(function(){
			//顯示出真正的牌
			$(".game_table_content > div > .card_wrap[card_type=" + value + "]").removeClass('card_transparent');

			//把假牌歸位
			$(".card_stack .card_wrap[card_type=" + value + "]").css('display','none'); //把牌隱藏
			$(".card_stack .card_wrap[card_type=" + value + "]").css("top",0 + "px");
			$(".card_stack .card_wrap[card_type=" + value + "]").css("left",0 + "px");
		}, 1000);

		setTimeout(function(){
			$(".card_stack .card_wrap[card_type=" + value + "]").css('display','block'); //把牌顯示
		}, 2000);
	});
	check_card_background(); //顯示牌的花色號碼
	next_step = 'step3';
	my_check = false;
	enemy_check = false;

	//根據大盲小盲切換回合
	if(decide_blind % 2 == 0){
		point_player = 'my';
		check_turn();
	}
	else{
		point_player = 'enemy';
		check_turn();
	}
}

function give_card_step3(){
	var next_card_type = ["public_card4"];

	next_card_type.forEach(function(value,index){
		var stack_card_top = $(".card_stack .card_wrap.card_stack_position").offset().top;
		var stack_card_left = $(".card_stack .card_wrap.card_stack_position").offset().left;
		var hand_card_top = $(".game_table_content > div > .card_wrap[card_type=" + value + "]").offset().top;
		var hand_card_left = $(".game_table_content > div > .card_wrap[card_type=" + value + "]").offset().left;

		//將牌發到指定位置
		$(".card_stack .card_wrap[card_type=" + value + "]").css("top",hand_card_top - stack_card_top + "px");
		$(".card_stack .card_wrap[card_type=" + value + "]").css("left",hand_card_left - stack_card_left + "px");

		setTimeout(function(){
			//顯示出真正的牌
			$(".game_table_content > div > .card_wrap[card_type=" + value + "]").removeClass('card_transparent');

			//把假牌歸位
			$(".card_stack .card_wrap[card_type=" + value + "]").css('display','none'); //把牌隱藏
			$(".card_stack .card_wrap[card_type=" + value + "]").css("top",0 + "px");
			$(".card_stack .card_wrap[card_type=" + value + "]").css("left",0 + "px");
		}, 1000);

		setTimeout(function(){
			$(".card_stack .card_wrap[card_type=" + value + "]").css('display','block'); //把牌顯示
		}, 2000);
	});
	check_card_background(); //顯示牌的花色號碼
	next_step = 'step4';
	my_check = false;
	enemy_check = false;

	//根據大盲小盲切換回合
	if(decide_blind % 2 == 0){
		point_player = 'my';
		check_turn();
	}
	else{
		point_player = 'enemy';
		check_turn();
	}
}

function give_card_step4(){
	var next_card_type = ["public_card5"];

	next_card_type.forEach(function(value,index){
		var stack_card_top = $(".card_stack .card_wrap.card_stack_position").offset().top;
		var stack_card_left = $(".card_stack .card_wrap.card_stack_position").offset().left;
		var hand_card_top = $(".game_table_content > div > .card_wrap[card_type=" + value + "]").offset().top;
		var hand_card_left = $(".game_table_content > div > .card_wrap[card_type=" + value + "]").offset().left;

		//將牌發到指定位置
		$(".card_stack .card_wrap[card_type=" + value + "]").css("top",hand_card_top - stack_card_top + "px");
		$(".card_stack .card_wrap[card_type=" + value + "]").css("left",hand_card_left - stack_card_left + "px");

		setTimeout(function(){
			//顯示出真正的牌
			$(".game_table_content > div > .card_wrap[card_type=" + value + "]").removeClass('card_transparent');

			//把假牌歸位
			$(".card_stack .card_wrap[card_type=" + value + "]").css('display','none'); //把牌隱藏
			$(".card_stack .card_wrap[card_type=" + value + "]").css("top",0 + "px");
			$(".card_stack .card_wrap[card_type=" + value + "]").css("left",0 + "px");
		}, 1000);

		setTimeout(function(){
			$(".card_stack .card_wrap[card_type=" + value + "]").css('display','block'); //把牌顯示
		}, 2000);
	});
	check_card_background(); //顯示牌的花色號碼
	next_step = 'end_game';
	my_check = false;
	enemy_check = false;

	//根據大盲小盲切換回合
	if(decide_blind % 2 == 0){
		point_player = 'my';
		check_turn();
	}
	else{
		point_player = 'enemy';
		check_turn();
	}
}


function check_card_background(){
	$(".card_wrap").each(function(index,value){
		var card_number = $(this).attr('card_number');
		if(card_number != undefined){ 
			$(this).find('.card_positive').css('background-image','url(images/' + card_number + '.png)');
		}
	});
}



function raise_chip(add_chip){
	add_chip = parseInt(add_chip, 10);
	if(add_chip == 0){
		alert('加注金額不能為 0');
		return;
	}

	if(point_player == 'my'){
		var enemy_chip_remind = $('.table_top_input').val(); //電腦的籌碼剩餘
		enemy_chip_remind = parseInt(enemy_chip_remind, 10);
		var my_chip = $(".my_chip .my_chip_value span").html();
		my_chip = parseInt(my_chip, 10);
		var enemy_chip = $(".enemy_chip .enemy_chip_value span").html();
		enemy_chip = parseInt(enemy_chip, 10);
		var final_raise_chip = my_chip + add_chip;
		if(final_raise_chip < enemy_chip){
			alert('加注金額不能小於對手籌碼喔!!');
			return;
		}
		else if(final_raise_chip > enemy_chip_remind){
			alert('加注金額不能大於對手剩餘金額喔!!');
			return;
		}

		$(".my_chip .my_chip_value span").html(final_raise_chip);
		
		//下面切換成對手回合
		point_player = 'enemy';
		check_turn();
	}
	else if(point_player == 'enemy'){
		var enemy_chip = $('.enemy_chip_value span').html(); //電腦的牌桌籌碼
		enemy_chip = parseInt(enemy_chip, 10);
		var my_chip = $('.my_chip_value span').html(); //玩家的牌桌籌碼
		my_chip = parseInt(my_chip, 10);
		var enemy_chip_remind = $('.table_top_input').val(); //電腦的籌碼剩餘
		enemy_chip_remind = parseInt(enemy_chip_remind, 10);
		var my_chip_remind = $('.table_bottom_input').val(); //玩家的籌碼剩餘
		my_chip_remind = parseInt(my_chip_remind, 10);
		
		//如果加注為-1的話 則all in
		if(add_chip == -1){
			if(enemy_chip_remind < my_chip_remind){
				var final_raise_chip = enemy_chip_remind;
			}
			else if(enemy_chip_remind > my_chip_remind){
				var	final_raise_chip = my_chip_remind;
			}
			else{
				var	final_raise_chip = my_chip_remind;
			}
		}
		else{
			var final_raise_chip = enemy_chip + add_chip;
		}

		if(final_raise_chip < my_chip){
			final_raise=mychip
		}

		$(".enemy_chip .enemy_chip_value span").html(final_raise_chip);
		
		//下面切換成對手回合
		point_player = 'my';
		check_turn();
	}
	else{
		alert('不  可  以 ! !');
		ruturn;
	}

	//紀錄回合log
	if(point_player == 'my'){
		turn_log = turn_log.concat([2, 0, add_chip]);
	}
	else if(point_player == 'enemy'){
		turn_log = turn_log.concat([2, 1, add_chip]);	
	}
	else{
		alert('不 可 能 ! !');
		return;
	}
}

function toggle_raise_interface(oc){
	if(oc == 'open'){
		$('.chip_form_wrap').css('display','block');
	}
	else{
		$('.chip_form_wrap').css('display','none');
		$('.chip_raise').html('0');
	}
}

function call_chip(){
	var my_chip = $(".my_chip .my_chip_value span").html(); //我的籌碼 嘻嘻
	my_chip = parseInt(my_chip, 10);
	var enemy_chip = $(".enemy_chip .enemy_chip_value span").html(); //對手的籌碼 嘻嘻
	enemy_chip = parseInt(enemy_chip, 10);
	if(my_chip < enemy_chip){
		$(".my_chip .my_chip_value span").html(enemy_chip);
	}
	else if(my_chip > enemy_chip){
		$(".enemy_chip .enemy_chip_value span").html(my_chip);
	}
	else{
		alert("Its pity.現在籌碼是一樣的哦，親");
		return;
	}

	//call botton 的判斷
	if(turn_number == 1){
		if(point_player == 'my'){
			point_player = 'enemy';
			check_turn();
		}
		else if(point_player == 'enemy'){
			point_player = 'my';
			check_turn();
		}
		else{
			alert("不 可 以 ! !");
			return;
		}
	}
	else{
		if(next_step == 'step2'){
			give_card_step2();
		}
		else if(next_step == 'step3'){
			give_card_step3();
		}
		else if(next_step == 'step4'){
			give_card_step4();
		}
		else if(next_step == 'end_game'){
			settlement_winner();
		}
		else{
			alert('不 可 能 ! !');
			return;
		}
	}

	//紀錄回合log
	if(point_player == 'my'){
		turn_log = turn_log.concat([3, 0, -1]);
	}
	else if(point_player == 'enemy'){
		turn_log = turn_log.concat([3, 1, -1]);	
	}
	else{
		alert('不 可 能 ! !');
		return;
	}
}

function check_turn(){
	if(point_player == 'my'){
		turn_number++;
		$('.my_turn').addClass('active');
		$('.enemy_turn').removeClass('active');
	}
	else if(point_player == 'enemy'){
		turn_number++;
		$('.enemy_turn').addClass('active');
		$('.my_turn').removeClass('active');

		enemy_data_post();    //讓敵人動作
	}
	else{
		alert("不 可 以 ! !");
		return;
	}
}


function checking_check(){
	if(my_check == false && enemy_check == false){ //以下判斷
		if(point_player == 'my'){
			my_check = true;

			point_player = 'enemy'; //切換回合
			check_turn();
		}
		else if(point_player == 'enemy'){
			enemy_check = true;

			point_player = 'my'; // 切換回合
			check_turn();
		}
		else{
			alert("不 可 以 ! !");
			return;
		}
															//ajax送資料
	}
	else if(my_check == true && enemy_check == false){
		enemy_check = true;
		//他按且發牌
		if(next_step == 'step2'){
			give_card_step2();
		}
		else if(next_step == 'step3'){
			give_card_step3();
		}
		else if(next_step == 'step4'){
			give_card_step4();
		}
		else if(next_step == 'end_game'){
			settlement_winner();
		}
		else{
			alert('不 可 能 ! !');
			return;
		}
	}
	else if(my_check == false && enemy_check == true){
		my_check = true;
		//我按且發牌
		if(next_step == 'step2'){
			give_card_step2();
		}
		else if(next_step == 'step3'){
			give_card_step3();
		}
		else if(next_step == 'step4'){
			give_card_step4();
		}
		else if(next_step == 'end_game'){
			settlement_winner();
		}
		else{
			alert('不 可 能 ! !');
			return;
		}
	}
	else if(my_check == true && enemy_check == true){
		alert("不 可 以 ! !");
		return;
	}

	//紀錄回合log
	if(point_player == 'my'){
		turn_log = turn_log.concat([4, 0, -1]);
	}
	else if(point_player == 'enemy'){
		turn_log = turn_log.concat([4, 1, -1]);	
	}
	else{
		alert('不 可 能 ! !');
		return;
	}
}

function toggle_fold_interface(oc){
	if(oc == 'open'){
		$('.fold_form_wrap').css('display','block');
	}
	else{
		$('.fold_form_wrap').css('display','none');
	}
}

function who_fold(loser){
	var enemy_chip_value = $('.enemy_chip_value span').html(); //電腦的牌桌籌碼
	enemy_chip_value = parseInt(enemy_chip_value, 10);
	var my_chip_value = $('.my_chip_value span').html(); //玩家的牌桌籌碼
	my_chip_value = parseInt(my_chip_value, 10);
	var enemy_chip_remind = $('.table_top_input').val(); //電腦的籌碼剩餘
	enemy_chip_remind = parseInt(enemy_chip_remind, 10);
	var my_chip_remind = $('.table_bottom_input').val(); //玩家的籌碼剩餘
	my_chip_remind = parseInt(my_chip_remind, 10);

	// 0是玩家輸，1是電腦輸。
	if(loser == '0'){
		alert('You lose!');
		enemy_chip_remind = enemy_chip_remind + my_chip_value;
		my_chip_remind = my_chip_remind - my_chip_value;
		$('.table_bottom_input').val(my_chip_remind);
		$('.table_top_input').val(enemy_chip_remind);
	}
	else if(loser == '1'){
		alert('You win!');
		my_chip_remind = my_chip_remind + enemy_chip_value;
		enemy_chip_remind = enemy_chip_remind - enemy_chip_value;
		$('.table_bottom_input').val(my_chip_remind);
		$('.table_top_input').val(enemy_chip_remind);
	}
	else{
		alert('不 可 能 ! !');
		return;
	}

	//紀錄回合log
	if(point_player == 'my'){
		turn_log = turn_log.concat([8, 0, -1]);
	}
	else if(point_player == 'enemy'){
		turn_log = turn_log.concat([8, 1, -1]);	
	}
	else{
		alert('不 可 能 ! !');
		return;
	}
	var my_chip_remind = $('.table_bottom_input').val();
	my_chip_remind = parseInt(my_chip_remind, 10);
	var com_chip_remind = $('.table_top_input').val();
	com_chip_remind = parseInt(com_chip_remind, 10);
	if(com_chip_remind<=0){
		alert("你徹底打敗電腦了 重整後再來一局吧");
	}
	if(my_chip_remind<=0){
		alert("輸給電腦並不可恥 重整後再來一局吧");
	}
	//enemy_data_post();
	
	//重置賽局
	decide_blind++;
	setTimeout(function(){
		init_game();
	}, 1500);
}

function enemy_data_post(){
	var all_card_type = ["enemy_card1","enemy_card2","my_card1","my_card2","public_card1","public_card2","public_card3","public_card4","public_card5"];
	var all_card_value = [];
	all_card_type.forEach(function(value,index){
		all_card_value[value] = $(".game_table_content > div > .card_wrap[card_type=" + value + "]").attr('card_number');
		all_card_value[value] = parseInt(all_card_value[value], 10) - 1; //調整成從0開始

		//以下是未翻開的牌更改為-1
		var check_card_transparent = $(".game_table_content > div > .card_wrap[card_type=" + value + "]").hasClass('card_transparent');
		if(check_card_transparent == true){
			all_card_value[value] = -1;
		}
	});
	var enemy_chip_value = $('.enemy_chip_value span').html(); //電腦的牌桌籌碼
	enemy_chip_value = parseInt(enemy_chip_value, 10);
	var my_chip_value = $('.my_chip_value span').html(); //玩家的牌桌籌碼
	my_chip_value = parseInt(my_chip_value, 10);
	var enemy_chip_remind = $('.table_top_input').val(); //電腦的籌碼剩餘
	enemy_chip_remind = parseInt(enemy_chip_remind, 10);
	var my_chip_remind = $('.table_bottom_input').val(); //玩家的籌碼剩餘
	my_chip_remind = parseInt(my_chip_remind, 10);
	
	//下面傳送
	var input_test = [
		all_card_value['public_card1'], all_card_value['public_card2'], all_card_value['public_card3'], all_card_value['public_card4'], all_card_value['public_card5'], //前五張牌只開到第四張，最後一張為-1
		all_card_value['enemy_card1'], all_card_value['enemy_card2'], //電腦的手排
		enemy_card_level,	// 接手牌的level值
		enemy_chip_value, //電腦的籌碼
		my_chip_value, //玩家的籌碼
	];
	var post_input = input_test;
	for(var i=post_input.length;i<14;i++){
		post_input[i] = -1;
	}
	console.log('AI post = ' + post_input);
		  //下面傳送
	$.ajax({
		type:'POST',
		url:'http://127.0.0.1:8080',
		data:{type:"predict",input:post_input },
		dataType:"json",
		success: function(data)
		{
			setTimeout(function(){
				console.log('AI receive = ' + data);
				if(turn_number <= 2){
					enemy_card_level = data[2];
				}
				
				var raise = data[1];
				
			    data = data[0];
				if(data == 2){	//加注 阿修!記得修這裡
					let_you_know_what_ai_do('Raise');
					var enemy_raise = my_chip_value + raise - enemy_chip_value;
					if(enemy_raise > my_chip_remind-my_chip_value){
						enemy_raise = my_chip_remind-my_chip_value;
					}
					raise_chip(enemy_raise);
					//
					/*
					var enemy_raise = my_chip_value + raise - enemy_chip_value;
					raise_chip(enemy_raise);
					if(enemy_chip_value > my_chip_remind){
						enemy_chip_value = my_chip_remind;
					}
					*/
				}
				else if(data == 3 || data == 4){ //檢查如果注碼一樣 call > check
					if(enemy_chip_value == my_chip_value){
						let_you_know_what_ai_do('Check');
						checking_check();
					}
					else{
						let_you_know_what_ai_do('Call');
						call_chip();
					}
				}
				else if(data == 8){      //棄牌
					let_you_know_what_ai_do('Fold');
					who_fold(1);
				}
				else if(data == 9){      //all in
					let_you_know_what_ai_do('All in ♥');
					raise_chip(-1);		 //raise_chip的remark如果是-1為 allin
				}
				else{
					alert(data);
				}
			}, 1500);
		},
		error: function()
		{
			console.log('error');
		}
	});
}

function settlement_winner(){
	var all_card_type = ["enemy_card1","enemy_card2","my_card1","my_card2","public_card1","public_card2","public_card3","public_card4","public_card5"];
	var all_card_value = [];
	all_card_type.forEach(function(value,index){
		
		//結算時將所有牌翻開
		$(".game_table_content > div > .card_wrap[card_type=" + value + "]").addClass('active');

		//抓取牌的編號 post
		all_card_value[value] = $(".game_table_content > div > .card_wrap[card_type=" + value + "]").attr('card_number');
		all_card_value[value] = parseInt(all_card_value[value], 10) - 1; //調整成從0開始
		
		//以下是未翻開的牌更改為-1
		var check_card_transparent = $(".game_table_content > div > .card_wrap[card_type=" + value + "]").hasClass('card_transparent');
		if(check_card_transparent == true){
			all_card_value[value] = -1;
		}
	});
	
	var input_test = [
		all_card_value['my_card1'], all_card_value['my_card2'],
		all_card_value['enemy_card1'], all_card_value['enemy_card2'],
		all_card_value['public_card1'], all_card_value['public_card2'], all_card_value['public_card3'], all_card_value['public_card4'], all_card_value['public_card5']
	];
	console.log(input_test);
	$.ajax({
		type:'POST',
		url:'http://127.0.0.1:8080',
		data:{type:"hands",input:input_test},
		success: function(data)
		{
			console.log('winner=' + data);
			settlement_chip(data);
		},
		error: function()
		{
		 //alert("Ajax錯誤!");
		}
	});
}
	
function settlement_chip(winner){
	var enemy_chip_value = $('.enemy_chip_value span').html(); //電腦的牌桌籌碼
	enemy_chip_value = parseInt(enemy_chip_value, 10);
	var my_chip_value = $('.my_chip_value span').html(); //玩家的牌桌籌碼
	my_chip_value = parseInt(my_chip_value, 10);
	var enemy_chip_remind = $('.table_top_input').val(); //電腦的籌碼剩餘
	enemy_chip_remind = parseInt(enemy_chip_remind, 10);
	var my_chip_remind = $('.table_bottom_input').val(); //玩家的籌碼剩餘
	my_chip_remind = parseInt(my_chip_remind, 10);

	// 0是玩家贏，1是電腦贏，2是平手
	if(winner == '0'){
		alert('You win!');
		my_chip_remind = my_chip_remind + enemy_chip_value;
		enemy_chip_remind = enemy_chip_remind - enemy_chip_value;
		$('.table_bottom_input').val(my_chip_remind);
		$('.table_top_input').val(enemy_chip_remind);
	}
	else if(winner == '1'){
		alert('You lose!');
		enemy_chip_remind = enemy_chip_remind + my_chip_value;
		my_chip_remind = my_chip_remind - my_chip_value;
		$('.table_bottom_input').val(my_chip_remind);
		$('.table_top_input').val(enemy_chip_remind);
	}
	else if(winner == '2'){
		alert('雙方平手，歸還籌碼');
	}
	else{
		alert('不 可 能 ! !');
		return;
	}
	var my_chip_remind = $('.table_bottom_input').val();
	my_chip_remind = parseInt(my_chip_remind, 10);
	var com_chip_remind = $('.table_top_input').val();
	com_chip_remind = parseInt(com_chip_remind, 10);
	if(com_chip_remind<=0){
		alert("你徹底打敗電腦了 重整後再來一局吧");
	}
	if(my_chip_remind<=0){
		alert("輸給電腦並不可恥 重整後再來一局吧");
	}
	//重置賽局
	decide_blind++;
	setTimeout(function(){
		init_game();
	}, 1500);
}

//讓玩家知道電腦在做什麼唷♥
function let_you_know_what_ai_do(text){
	$('.enemy_action').html(text);
	$('.enemy_action').addClass('active');
	setTimeout(function(){
		$('.enemy_action').removeClass('active');
	}, 1250);
}

//------------------按鈕功能------------------
$('.botton_wrap1').click(function(){ //按下raise 啟動加注介面
	if(point_player == 'enemy') return; //檢查是不是我ㄉ回合
	toggle_raise_interface('open');
	var com_raise = $('.enemy_chip_value span').html(); //抓取當前加注的籌碼金額
	com_raise = parseInt(com_raise, 10);
	var player_raise = $('.my_chip .my_chip_value span').html();
	player_raise = parseInt(player_raise, 10);
	var now_raise = com_raise+player_raise;
	document.getElementById("chip_pool").innerHTML = now_raise
});
$('.chip_botton_cancel').click(function(){ //取消加注介面
	toggle_raise_interface('none'); 
});
$('.chip_botton').click(function(){ //加注
	var add_raise_text = $(this).html(); //抓取加注的按鈕金額
	var add_raise=0;
	var my_chip_value = $(".my_chip .my_chip_value span").html();
	my_chip_value = parseInt(my_chip_value, 10);
	var enemy_max_chip = $('.table_top_input').val();//電腦剩餘
	enemy_max_chip = parseInt(enemy_max_chip, 10);
	var my_max_chip = $('.table_bottom_input').val();//玩家剩餘
	my_max_chip = parseInt(my_max_chip, 10);
	if(add_raise_text[0]=='2'){
		add_raise=2;
	}
	else if(add_raise_text[0]=='3'){
		add_raise=3;
	}
	else if(add_raise_text[0]=='A'){
		var max_chip = (enemy_max_chip > my_max_chip) ? my_max_chip : enemy_max_chip;
		add_raise = max_chip - my_chip_value;
	}

	var com_raise = $('.enemy_chip_value span').html(); //抓取當前加注的籌碼金額
	com_raise = parseInt(com_raise, 10);
	var player_raise = $('.my_chip .my_chip_value span').html();
	player_raise = parseInt(player_raise, 10);
	var now_raise = com_raise+player_raise;//計算池底
	console.log(now_raise) 
	var final_raise = add_raise * now_raise;//最後計算

	var max_chip = (enemy_max_chip > my_max_chip) ? my_max_chip : enemy_max_chip;
	max_chip = max_chip - my_chip_value;
	
	if(final_raise > max_chip){
		document.getElementById("chip_raise_numb").value = max_chip;
	}
	else{
		document.getElementById("chip_raise_numb").value = final_raise;
	}
	if(add_raise_text[0]=='重'){
		document.getElementById("chip_raise_numb").value = 0;
	}
});
$('.chip_botton_confirm').click(function(){ //確定的按鈕功能
	var enter_raise = document.getElementById("chip_raise_numb").value
	var now_raise = enter_raise;
	raise_chip(now_raise);
	toggle_raise_interface('none');

});
$('.botton_wrap2').click(function(){  //跟注功能
	if(point_player == 'enemy') return;
	call_chip();
});

$('.botton_wrap3').click(function(){
	if(point_player == 'enemy') return; //檢查是不是我ㄉ回合
	var my_chip_value = $(".my_chip .my_chip_value span").html();//檢查籌碼是否相同，可以開啟check按鍵
	my_chip_value = parseInt(my_chip_value, 10);
	var enemy_chip_value = $(".enemy_chip .enemy_chip_value span").html();
	enemy_chip_value = parseInt(enemy_chip_value, 10);
	if(my_chip_value != enemy_chip_value){
		return;
	}
	
	checking_check();
});

$('.botton_wrap4').click(function(){
	if(point_player == 'enemy') return;
	toggle_fold_interface('open');
});

$('.fold_botton_cancel').click(function(){ //取消加注介面
	toggle_fold_interface('none');
});

$('.fold_botton_confirm').click(function(){
	if(point_player == 'enemy') return;
	who_fold(0);
	toggle_fold_interface('none');
});


//------------------執行區------------------
init_card();
init_game(); 
//-----------------------------------
var test1 = "a"+"b"+"c";
var test2 = 123;
var next_card_type = ["enemy_card1","enemy_card2","my_card1","my_card2"];
var test3 = ".card_wrap enemy_card1";
var test4 = ".card_wrap " + next_card_type[0];
next_card_type.forEach(function(index,value){
	var test5 = ".card_wrap " + value;
});
//---------