<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
    <title>plind.us - Recipes: <xsl:value-of select="recipe/name"/></title>
    <link rel="stylesheet" type="text/css" href="/css/global.css"/>
    <link rel="icon" type="image/ico" href="/favicon.ico" sizes="16x16 32x32"/>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
  </head>
  <body>
    <div id="page-wrapper">
      <header>
        <div class="header-title"><a href="https://www.plind.us">plind.us</a></div>
      </header>
      <nav>
        <div class="nav-path">
          <a href="/"><span class="no-underline">&#127968; </span>Home</a> / <a href="/">Recipes</a> / <xsl:value-of select="recipe/name"/>
        </div>
      </nav>
      <main>
  	   <h1><xsl:value-of select="recipe/name"/></h1>
       <xsl:if test="recipe/summary">
       <p><xsl:value-of select="recipe/summary"/></p>
       </xsl:if>
       <ul>
         <li>Servings: <xsl:value-of select="recipe/servings"/></li>
         <li>Difficulty: <xsl:value-of select="recipe/difficulty"/></li>
         <li>Time: <xsl:value-of select="recipe/time"/></li>
       </ul>
       <h2>Ingredients</h2>
       <ul>
         <xsl:for-each select="recipe/ingredients/ingredient">
         <li><xsl:value-of select="concat(amount, ' ')"/><xsl:value-of select="description"/></li>
         </xsl:for-each>
       </ul>
       <h2>Directions</h2>
       <xsl:for-each select="recipe/directions/step">
       <h3>Step <xsl:value-of select="@number"/></h3>
       <p><xsl:value-of select="description"/></p>
       </xsl:for-each>
       <xsl:if test="recipe/tips">
       <h2>Tips &amp; Ideas</h2>
       <ul>
       <xsl:for-each select="recipe/tips/tip">
         <li><xsl:value-of select="description"/></li>
       </xsl:for-each>
     </ul>
       </xsl:if>
       <xsl:if test="recipe/nutrition">
       <h2>Nutrition Information</h2>
       <ul>
         <li>Calories: <xsl:value-of select="recipe/nutrition/calories/value"/><xsl:value-of select="recipe/nutrition/calories/unit"/></li>
         <li>Fat: <xsl:value-of select="recipe/nutrition/fat/value"/><xsl:value-of select="recipe/nutrition/fat/unit"/></li>
         <li>Saturated Fat: <xsl:value-of select="recipe/nutrition/saturated_fat/value"/><xsl:value-of select="recipe/nutrition/saturated_fat/unit"/></li>
       </ul>
       </xsl:if>
       <xsl:if test="recipe/source">
       <h2>Source</h2>
       <p><xsl:text>"</xsl:text><xsl:value-of select="recipe/source/publication"/><xsl:text>" </xsl:text><i><xsl:value-of select="recipe/source/title"/></i><xsl:text>, </xsl:text><a href="{recipe/source/url}"><xsl:value-of select="recipe/source/url"/></a><xsl:text>.  Accessed </xsl:text><xsl:value-of select="recipe/source/date_accessed"/><xsl:text>.</xsl:text></p>
       </xsl:if>
     </main>
     <footer>
       <p class="footer-updated">Last updated: <em>2024-03-12 23:12:26</em></p>
       <p class="footer-license"><a href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 Int'l License</a></p>
       <br/>
     </footer>
   </div>
 </body>
 </html>
</xsl:template>

</xsl:stylesheet>
