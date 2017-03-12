var isMobile={Android:function(){return navigator.userAgent.match(/Android/i);},BlackBerry:function(){return navigator.userAgent.match(/BlackBerry/i);},iOS:function(){return navigator.userAgent.match(/iPhone|iPad|iPod/i);},Opera:function(){return navigator.userAgent.match(/Opera Mini/i);},Windows:function(){return navigator.userAgent.match(/IEMobile/i);},any:function(){return(isMobile.Android()||isMobile.BlackBerry()||isMobile.iOS()||isMobile.Opera()||isMobile.Windows());}};(function($){'use strict';$('.carousel').carousel({pause:'none',interval:7000})
var equalheight,topPostion,currentDiv,rowDivs;equalheight=function(container){var currentTallest=0,currentRowStart=0,rowDivs=new Array(),$el,topPosition=0;$(container).each(function(){$el=$(this);$($el).height('auto')
topPostion=$el.position().top;if(currentRowStart!=topPostion){for(currentDiv=0;currentDiv<rowDivs.length;currentDiv++){rowDivs[currentDiv].height(currentTallest);}
rowDivs.length=0;currentRowStart=topPostion;currentTallest=$el.height();rowDivs.push($el);}else{rowDivs.push($el);currentTallest=(currentTallest<$el.height())?($el.height()):(currentTallest);}
for(currentDiv=0;currentDiv<rowDivs.length;currentDiv++){rowDivs[currentDiv].height(currentTallest);}});}
function sliderHt(){var winH=$(window).innerHeight();$('#homeSlider').css("height",winH);}
function carIndiRepos(){var winH=$('#homeSlider').innerHeight();var carH=$('#homeSlider .carousel-indicators').height();$('#homeSlider .carousel-indicators').css('margin-top','-'+carH/2+'px');$('#homeSlider .carousel-indicators').css('top',winH/2+'px');}
function btnHover(){$('.btn').each(function(){var thisBtn=$(this);if(thisBtn.find('i')){var thisSpan=thisBtn.find('i').clone();thisBtn.append(thisSpan.addClass('hover'));}});}
function loadVid(){var vidUrl=$('#video a.icon').attr('href');var vidFrame='<iframe width="" height="" src="'+vidUrl+'?autoplay=1&loop=1&rel=0?wmode=xxxx" frameborder="0" allowfullscreen></iframe>';$('#video .videoBox').append(vidFrame);}
function autoVcnter(elm){var elmH=$(elm).innerHeight();$(elm).css("margin-top","-"+elmH/2+'px');}
function vidRePos(){var winW=$('body').width();if(winW<=850){var getTopMargin=$('#video .textBox').height();$('#video .videoBox').css('margin-top',getTopMargin+'px');}else{$('#video .videoBox').css('margin-top','0px');}}
$('#contentBox .owl-carousel').owlCarousel({loop:true,rewind:false,margin:0,animateIn:'fadeInLeft',animateOut:'fadeOutDown',autoplay:true,autoplayTimeout:5000,autoplayHoverPause:true,nav:true,navText:["<img class='svg' src='images/svg/arrow-left-w.svg' onerror='this.src='arrow-left-w.png' alt='Prev' />","<img class='svg' src='images/svg/arrow-right-w.svg' onerror='this.src='arrow-right-w.png'' alt='Next' />"],responsiveClass:true,responsive:{0:{items:1,nav:true},600:{items:1,nav:true},1000:{items:1,nav:true}}});$('#testimonial .owl-carousel').owlCarousel({center:true,loop:true,rewind:false,margin:0,animateIn:'fadeIn',animateOut:'fadeOut',autoplay:true,autoplayTimeout:5000,autoplayHoverPause:true,dots:false,nav:true,navText:["<img class='svg' src='images/svg/arrow-left-w.svg' onerror='this.src='arrow-left-w.png' alt='Prev' />","<img class='svg' src='images/svg/arrow-right-w.svg' onerror='this.src='arrow-right-w.png'' alt='Next' />"],responsiveClass:true,responsive:{0:{items:1,nav:true},600:{items:1,nav:true},1000:{items:1,nav:true}}});var fixWidth=$('body').hasClass('fixWidth');if(fixWidth){$('#gallery .owl-carousel').owlCarousel({center:true,loop:true,rewind:false,margin:0,autoplay:true,autoplayTimeout:5000,autoplayHoverPause:true,responsiveBaseElement:window,dots:false,nav:true,navText:["<img class='svg' src='images/svg/arrow-left-w.svg' onerror='this.src='arrow-left-w.png' alt='Prev' />","<img class='svg' src='images/svg/arrow-right-w.svg' onerror='this.src='arrow-right-w.png'' alt='Next' />"],responsiveClass:true,responsive:{0:{items:2,nav:true},600:{items:3,nav:false},1000:{items:4,nav:true},1201:{items:4,nav:true}}});}else{$('#gallery .owl-carousel').owlCarousel({center:true,loop:true,rewind:false,margin:0,autoplay:true,autoplayTimeout:5000,autoplayHoverPause:true,responsiveBaseElement:window,dots:false,nav:true,navText:["<img class='svg' src='images/svg/arrow-left-w.svg' onerror='this.src='arrow-left-w.png' alt='Prev' />","<img class='svg' src='images/svg/arrow-right-w.svg' onerror='this.src='arrow-right-w.png'' alt='Next' />"],responsiveClass:true,responsive:{0:{items:2,nav:true},600:{items:3,nav:false},1000:{items:4,nav:true},1400:{items:6,nav:true}}});}
$(window).load(function(){var preLodr=$('#preloader');if(preLodr){$('#preloader').fadeOut();$('.loading').delay(350).fadeOut('slow');$('body').delay(350).css({'overflow':'visible'});}
if(equalheight){equalheight('.equal, .member, #testimonial .owl-item .item');}
var winW=$('body').width();if(winW>=1024){sliderHt();}
if(winW<=767){$('nav a[href^=#], a.top[href^=#], a.smooth[href^=#]').on("click",function(event){event.preventDefault();$('html,body').animate({scrollTop:$(this.hash).offset().top- 0},1000);});}else{$('nav a[href^=#], a.top[href^=#], a.smooth[href^=#]').on("click",function(event){event.preventDefault();$('html,body').animate({scrollTop:$(this.hash).offset().top- 0},1000);});}
var carI=$('#homeSlider .carousel-indicators').length;if(carI>0){carIndiRepos();}
var btnHovr=$('.btn');if(btnHovr){btnHover();}
var contactForm=$('#contact');if(contactForm){$('#contact .form-control').on('focus',function(){$('#contact .form-group').removeClass('active');$(this).parent('.form-group').addClass('active');});$('#contact .form-control').on('blur',function(){$('#contact .form-group').removeClass('active');});}
autoVcnter('.textBox');var vidUrl=$('#video a.icon').attr('href');if(vidUrl){$('#video a.icon').on("click",function(event){event.preventDefault();if($('#video').hasClass('vidLoaded')){$('#video').removeClass('vidLoaded');setTimeout(function(){$('#video .videoBox').html('');},800);}else{$('#video').addClass('vidLoaded');loadVid();}});}
vidRePos();});$(window).resize(function(){if(equalheight){equalheight('.equal, .member, #testimonial .owl-item .item');}
var winW=$('body').width();if(winW>=1024){sliderHt();}
var carI=$('#homeSlider .carousel-indicators').length;if(carI>0){carIndiRepos();}
autoVcnter('.textBox');vidRePos();});$(window).on('scroll',function(){if($(window).scrollTop()>1000){$('a.top').fadeIn('slow');}else{$('a.top').fadeOut('slow');}});$('body').scrollspy({target:'#menu'});var wow=new WOW({boxClass:'wow',animateClass:'animated',offset:150,mobile:true,live:true})
wow.init();$('#nav-expander').on('click',function(e){e.preventDefault();$('body').toggleClass('nav-expanded');});$('#nav-close, .main-menu > li > a').on('click',function(e){e.preventDefault();$('body').removeClass('nav-expanded');});$('[data-toggle="tooltip"]').tooltip();function doAnimations(elems){var animEndEv='webkitAnimationEnd animationend';elems.each(function(){var $this=$(this),$animationType=$this.data('animation');$this.addClass($animationType).one(animEndEv,function(){$this.removeClass($animationType);});});}
var $myCarousel=$('#homeSlider'),$firstAnimatingElems=$myCarousel.find('.item:first').find("[data-animation ^= 'animated']");$myCarousel.carousel();doAnimations($firstAnimatingElems);$myCarousel.carousel('pause');$myCarousel.on('slide.bs.carousel',function(e){var $animatingElems=$(e.relatedTarget).find("[data-animation ^= 'animated']");doAnimations($animatingElems);});$("a[data-rel^='prettyPhoto']").prettyPhoto({overlay_gallery:true});$('input, textarea').placeholder();if(!isMobile.any()){$(window).stellar({horizontalScrolling:false,responsive:true});}
$('.stat').waypoint(function(){var ranges=[{divider:1e9,suffix:'G'},{divider:1e6,suffix:'M'},{divider:1e3,suffix:'k'}];function formatNumber(n){for(var i=0;i<ranges.length;i++){if(n>=ranges[i].divider){return(n/ranges[i].divider).toString()+ ranges[i].suffix;}}
return n.toString();}
$('.timer').removeClass('statEnd');$('.timer').countTo({refreshInterval:50,formatter:function(value,options){return value.toFixed(options.decimals);},onComplete:function(value){console.debug(this);$('.timer').each(function(){var statVal=$(this).attr('data-to');$(this).addClass('statEnd').html(formatNumber(statVal));});}});var lightLayout=$('body').hasClass('light');if(lightLayout){$('.chart').easyPieChart({scaleColor:false,lineWidth:1,barColor:'#6961ff',trackColor:'#f0efff',size:133});}else{$('.chart').easyPieChart({scaleColor:false,lineWidth:5,barColor:'#6961ff',trackColor:'#f0efff',size:133});}},{offset:'50%'});$('.panel-title a').on("click",(function(){var thisParent=$(this).parent().parent().next();if(thisParent.hasClass('in')){$(this).parent().removeClass('active');$(this).parent().parent().parent().removeClass('active');}else{$('.panel-title').removeClass('active');$('.panel-default').removeClass('active');$(this).parent().addClass('active');$(this).parent().parent().parent().addClass('active');}}));var sub_submitMessage="You have subscribed successfully.";var sub_successBoxColor="00c853";var sub_successBoxBorderStyle="solid";var sub_successBox_Border_Color="00c853";var sub_textColor="fff";$("#subscribeForm input").on("focus",(function(){$(this).prev("label").hide();$(this).prev().prev("label").hide();}));$("#subscribeForm").submit(function(){var emailSubscribe=$("#emailSubscribe").val();if(emailSubscribe==""){$('#emailSubscribe').addClass('reqfld');$('<span class="error" style="display:none; color: #F30;"><i class="fa fa-exclamation-circle"></i></span>').insertBefore('#emailSubscribe').fadeIn(400);$("#emailSubscribe").on("focus",(function(){$('#emailSubscribe').removeClass('reqfld');$(this).prev().fadeOut(400);}));return false;}else if(emailSubscribe.indexOf('@')==-1||emailSubscribe.indexOf('.')==-1){$('#emailSubscribe').addClass('reqfld');$('<span class="error" style="display:none;  color:#f30">Invalid!</span>').insertBefore('#emailSubscribe').fadeIn(400);$("#emailSubscribe").on("focus",(function(){$('#emailSubscribe').removeClass('reqfld');$(this).prev().fadeOut(400);}));return false;}
var sub_security=$("#sub-security").val();var dataString='&emailSubscribe='+ emailSubscribe+'&sub-security='+ sub_security;$.ajax({type:"POST",url:"form/subscribe.php",data:dataString,success:function(){$("#subscribeForm .form-row").hide();$('#subscribeForm').append("<div id='subscribesuccess' class='alert alert-success' style='border:#"+sub_successBox_Border_Color+" 1px "+sub_successBoxBorderStyle+"; background:#"+sub_successBoxColor+";' ></div>");$('#subscribesuccess').html("<h5 class='text-center' style='color:#"+sub_textColor+"; margin: 0'><i class='fa fa-check-circle'></i> "+sub_submitMessage+"</h5>").hide().delay(300).fadeIn(1500);$('#subscribeForm .form-row').delay(6000).slideUp('fast');}});return false;});$("#cfSlide").slider({value:1,min:1,max:100,step:1,slide:function(event,ui){$("#cfsVal").val(ui.value);var sval=$("#cfsVal").val();if(sval==100){$('#cfSubmit').removeAttr("disabled");}else{$('#cfSubmit').attr('disabled','disabled');}}});$("#cfSubmit").on("click",function(){var proceed=true;var output='';$("#cForm input[required], #cForm textarea[required]").each(function(){$(this).css('border-color','');if(!$.trim($(this).val())){$(this).css('border-color','red');proceed=false;}
var email_reg=/^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;if($(this).attr("type")=="email"&&!email_reg.test($.trim($(this).val()))){$(this).css('border-color','red');proceed=false;}});if(proceed){var post_data={'name':$('input[name=name]').val(),'email':$('input[name=email]').val(),'message':$('textarea[name=message]').val(),'domain':$(location).attr('href')}
$.post('form/contact.html',post_data,function(response){if(response.type=='error'){output='<div class="alert alert-warning alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+response.text+'</div>';}else{output='<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+response.text+'</div>';$("#cForm  input[required=true], #cForm textarea[required=true]").val('');$(".cfs_response").slideUp();}
$(".cfs_response").hide().html(output).slideDown();},'json');}});$("#cForm  input[required=true], #cForm textarea[required=true]").keyup(function(){$(this).css('border-color','');$(".cfs_response").slideUp();});}(jQuery));