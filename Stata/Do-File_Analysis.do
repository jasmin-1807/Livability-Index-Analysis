
  // Robustness Check with AARP Index 
  
  import delimited "/Users/jasmin/Desktop/Livability Score Data/Salary Datensätze Varianten/ComparisonwithOriginalIndex.csv", clear
  
   asdoc pwcorr orig_overallscore overallscore orig_housingscore housingscore orig_neighborhoodscore neighborhoodscore orig_transportationscore transportationscore orig_environmentscore environmentscore orig_healthscore healthscore orig_engagementscore engagementscore orig_opportunityscore opportunityscore, sig save(robustnessCheckOrig.doc)



// importing the data set
import delimited "/Users/jasmin/Desktop/Livability Score Data/Salary Datensätze Varianten/Gefilterte_Daten_2015_2019_Standorte_dynamic_StataPartsofHandT.csv", clear
 
 // setting the panel_id
 egen panel_id = group(company location)
 
// panel structure
 xtset panel_id year
 
 // dropping all salary value with one observation 
 drop if count == 1
 
 // generating dummy year variables
 tab year, gen (d_year)
 
 // descriptive Statistics 
  asdoc summarize year salary count fips overallscore healthscore neighborhoodscore opportunityscore environmentscore engagementscore housingscore transportationscore costoflivingindex total_incompany v22 avgmobyscore panel_id, label save(deskriptive_statistiken.doc)
  
 
 // pairwise correlation matrix 
  asdoc pwcorr salary overallscore healthscore neighborhoodscore opportunityscore environmentscore engagementscore housingscore transportationscore costoflivingindex total_incompany v22 avgmobyscore, sig save(correlations.doc)

 
 // renaming labels
  label variable salary "Salary in USD"

  label variable overallscore "Livability Score"

  label variable costoflivingindex "Cost of Living Index"

  label variable v22 "New Games"

  label variable avgmobyscore "MobyScore"

  label variable total_incompany "Company Size"

  label variable panel_id "Company+Location"

  label variable d_year1 "Dummy 2015"

  label variable d_year2 "Dummy 2016"

  label variable d_year3 "Dummy 2017"

  label variable d_year4 "Dummy 2018"

 
 // fixed effects Livability Score
 xtreg salary overallscore costoflivingindex v22 avgmobyscore total_incompany d_year*, fe vce(cluster panel_id)
  
  
  // export in Word
  asdoc xtreg salary overallscore costoflivingindex v22 avgmobyscore total_incompany d_year*, fe vce(cluster panel_id) save(NEW.doc) stars(0.001 0.01 0.05) label
  
  
// fixed effects Categories & Export 

 asdoc xtreg salary healthscore neighborhoodscore opportunityscore environmentscore engagementscore housingscore transportationscore costoflivingindex v22 avgmobyscore total_incompany d_year*, fe vce(cluster panel_id) save(NEW.doc) stars(0.001 0.01 0.05) label
 

  
  // random effects for Sargan Hansen statistic
  xtreg salary overallscore costoflivingindex v22 avgmobyscore total_incompany d_year1 d_year2 d_year3 d_year4, re vce(cluster panel_id)
  
  // testing
  xtoverid
  


 


  
  
  