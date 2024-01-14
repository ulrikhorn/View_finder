library(leaflet)
library(sp)
library(splitr)
library(lubridate)
library(here)
library(data.table)
library(ggrepel)
library(tidyverse)
library(ggmap)
library(gridExtra)
library(htmltools)
library(googleway)
library(magrittr)
library(zoo)
library(raster)
library(terrainr)
#register_google(key = "AIzaSyAnvWtAXCTpMvjoC9pms2XruLdIrq4kjSY") ## IKKE BRUK, JOSTEIN SIN



f= function(r_value, start_long, start_lat){
df <- data.frame()
  for (r in seq(from = 0, to = 0.2, by = r_value)) {
    test <- data.frame(
      lon = c(
        start_long+r*cos(10*pi/180),
        start_long+r*cos(20*pi/180),
        start_long+r*cos(pi/6),
        start_long+r*cos(40*pi/180),
        start_long+r*cos(50*pi/180),
        start_long+r*cos(pi/3),
        start_long+r*cos(70*pi/180),
        start_long+r*cos(80*pi/180),
        start_long+r*cos(pi/2),
        start_long+r*cos(100*pi/180),
        start_long+r*cos(110*pi/180),
        start_long+r*cos(2*pi/3),
        start_long+r*cos(130*pi/180),
        start_long+r*cos(140*pi/180),
        start_long+r*cos(5*pi/6),
        start_long+r*cos(160*pi/180),
        start_long+r*cos(170*pi/180),
        start_long+r*cos(pi),
        start_long+r*cos(190*pi/180),
        start_long+r*cos(200*pi/180),
        start_long+r*cos(7*pi/6),
        start_long+r*cos(220*pi/180),
        start_long+r*cos(230*pi/180),
        start_long+r*cos(4*pi/3),
        start_long+r*cos(250*pi/180),
        start_long+r*cos(260*pi/180),
        start_long+r*cos(3*pi/2),
        start_long+r*cos(280*pi/180),
        start_long+r*cos(290*pi/180),
        start_long+r*cos(5*pi/3),
        start_long+r*cos(310*pi/180),
        start_long+r*cos(320*pi/180),
        start_long+r*cos(11*pi/6),
        start_long+r*cos(340*pi/180),
        start_long+r*cos(350*pi/180),
        start_long+r*cos(2*pi)
      ) ,
      lat = c(
        start_lat+r*sin(10*pi/180),
        start_lat+r*sin(20*pi/180),
        start_lat+r*sin(pi/6),
        start_lat+r*sin(40*pi/180),
        start_lat+r*sin(50*pi/180),
        start_lat+r*sin(pi/3),
        start_lat+r*sin(70*pi/180),
        start_lat+r*sin(80*pi/180),
        start_lat+r*sin(pi/2),
        start_lat+r*sin(100*pi/180),
        start_lat+r*sin(110*pi/180),
        start_lat+r*sin(2*pi/3),
        start_lat+r*sin(130*pi/180),
        start_lat+r*sin(140*pi/180),
        start_lat+r*sin(5*pi/6),
        start_lat+r*sin(160*pi/180),
        start_lat+r*sin(170*pi/180),
        start_lat+r*sin(pi),
        start_lat+r*sin(190*pi/180),
        start_lat+r*sin(200*pi/180),
        start_lat+r*sin(7*pi/6),
        start_lat+r*sin(220*pi/180),
        start_lat+r*sin(230*pi/180),
        start_lat+r*sin(4*pi/3),
        start_lat+r*sin(250*pi/180),
        start_lat+r*sin(260*pi/180),
        start_lat+r*sin(3*pi/2),
        start_lat+r*sin(280*pi/180),
        start_lat+r*sin(290*pi/180),
        start_lat+r*sin(5*pi/3),
        start_lat+r*sin(310*pi/180),
        start_lat+r*sin(320*pi/180),
        start_lat+r*sin(11*pi/6),
        start_lat+r*sin(340*pi/180),
        start_lat+r*sin(350*pi/180),
        start_lat+r*sin(2*pi)
      ), 
      groups = seq(from = 1, to =36)
      
    )
    df <- bind_rows(df, test)
  }
  df
  
}


elev_test <- function(start_df = view_point, line_df = coords){
  
  #api_key <- "AIzaSyAnvWtAXCTpMvjoC9pms1XRuLdIRq4kjSY"
  initial_elevation <- google_elevation(df_locations = start_df, key = api_key)
  
  nchar(line_df[1:270,1:2]) %>% sum

  
  line_df1 <- line_df[1:252,]
  line_df2 <- line_df[253:504,]
  line_df3 <- line_df[505:756,]
  
  # line_df1 <- line_df[1:2,]
  # line_df2 <- line_df[253:504,]
  # line_df3 <- line_df[505:756,]
  
  test1 <- google_elevation(df_locations = line_df1, key = api_key)
  #Sys.sleep(1)
  test2 <- google_elevation(df_locations = line_df2, key = api_key)
  #Sys.sleep(1)
  test3 <- google_elevation(df_locations = line_df3, key = api_key)
  test <- bind_rows(test1, test2, test3)
  
  test <- test$results
  test$lat <- test$location$lat
  test$lon <- test$location$lng
  #colnames(test) <- c("elevation", "lat", "lon", "resolution")
  test <- test %>% mutate(higher = ifelse(elevation > initial_elevation$results$elevation, TRUE, FALSE))
  test$groups <- rep(seq(from = 1, to = 36), times = nrow(test)/36) # This needs to change if more angles are included
  test$iteration <- rep(seq(from = 1, to = nrow(test)/36), each = 36)
  
  test$include <- rep(FALSE, times = nrow(test))
  
  df <- data.frame()
  
  for (group_i in seq_along(unique(test$groups))) {
    t <-
      test %>% filter(groups == group_i) # Make new df for each line/angle
    true_vector <- which(t$higher)
    
    for (trues in seq_along(true_vector)) {
      if (t$elevation[true_vector[trues]] >= max(t$elevation[true_vector[1:trues]])) {
        
        t$include[true_vector[trues]] <- TRUE
        #df <- bind_rows(df, t)
      }
    }
    if(length(which(t$include == TRUE)) >= 1){
      t$include[1:which(t$include == TRUE)[1]] <- TRUE
    }else{
      t$include[1:length(t$include)] <- TRUE
    }
    
    df <- bind_rows(df, t)
  }

  
  
  df %>% filter(include ==  TRUE)
  
}


view_point <- data.frame(lat = 61.0349, lon = 7.8862)
view_point <- data.frame(lat = 60.3269, lon = 9.4880)

coords <- f(start_lat = view_point$lat, view_point$lon, r_value = 0.01)

elev_df <- elev_test(start_df = view_point, line_df = coords)


leaflet() %>% setView(lat = view_point$lat, lng = view_point$lon, zoom=10) %>% addProviderTiles(providers$OpenTopoMap) %>% 
  addCircles(data = elev_df, lng = ~lon, lat = ~lat, label = ~groups, radius = 2, color = "red")

f(start_lat = 61.0349, start_long = 7.8862,r_value = 0.01)
