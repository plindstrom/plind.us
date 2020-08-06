<?php
require("../www-bin/inc-global.php");

Page_Init("");
Page_Header(0);
?>
	<main>
		<div class="satori" id="satori"></div>
		<p>Hello, my name is Peter and welcome to my personal web site.  When I&rsquo;m not busy at work I enjoy cooking (well, eating mostly), reading a good book, watching slightly too much TV and relaxing at home. Beyond this web site you can find me at the usual places like <a href="https://www.linkedin.com/in/pclindstrom">LinkedIn</a>.</p>
		<p>How about some fun(ish) facts:</p>
		<ul class="list-standard">
			<li>I&rsquo;m currently reading <a href="https://www.goodreads.com/book/show/7677.Jurassic_Park"><em>Jurassic Park</em></a> by Michael Crichton</li>
			<li>The weather at home is <?php echo Get_Wx(); ?></li>
			<li>When I was born <?php echo Get_Fact(); ?></li>
		</ul>
	</main>
<?php
Page_Footer();
Page_End();
?>
