# 2 September 2019 version 1.0
# @author: jonathan t lee - https://github.com/jontaklee

#library(rstudioapi)
library(randomForest)
library(shiny)
library(shinydashboard)
library(tidyverse)

setwd(dirname(rstudioapi::getSourceEditorContext()$path))

cardlist <- read_csv('tron_cards.csv')
model <- readRDS('tron_rf_model.rds')
hand_comps <- read_csv('london_sims_RandomForest.csv')
ref_df <- read.csv('simulated_results.csv')[0,]

# render image for each card of a given type, taken from gatherer
render_imgs <- function(card_type) {
  card_ids <- cardlist %>%
    filter(type == card_type) %>%
    select(name, gatherer_id)
  
  lapply(1:nrow(card_ids), function(i){
    url <- paste("<img src='https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=",
                 as.character(card_ids$gatherer_id[i]),
                 "&type=card' height='150px'>", sep = '')
    column(width = 2, HTML(url))
  })
}

# render numericInput boxes for each card
render_inputs <- function(card_type) {
  card_ids <- cardlist %>%
    filter(type == card_type) %>%
    select(name, gatherer_id)
  
  lapply(1:nrow(card_ids), function(i){
    column(width = 2,
           numericInput(inputId = gsub(' ', '_', card_ids$name[i]),
                        label = NULL,
                        value = 0,
                        min = 0,
                        max = 4,
                        width = '75px'))
  })
}

# format all card count inputs
count_hand <- function(input) {
  count_table <- cardlist %>% select(name)
  
  counts <- vector()
  for (i in 1:nrow(count_table)) {
    input_name <- gsub(' ', '_', count_table$name[i])
    if (is.null(input[[input_name]])) {
      counts[i] <- 0
    } else {
      counts[i] <- input[[input_name]]
    }
  }
  
  count_table$counts <- counts
  return(count_table)
}

# determine the starting seven from user input
get_opener <- function(count_table) {
  hand <- lapply(1:nrow(count_table), function(i) {
    rep(count_table$name[i], count_table$counts[i])
  })
  hand <- unlist(hand)
  
  # dummy code for testing. Replace with real error raise
  if (length(hand) == 7) {
    return(hand)
  } else {
    return(c('Urzas Mine', 'Urzas Tower', 'Relic of Progenitus', 'Forest', 
             'Wurmcoil Engine', 'Sylvan Scrying', 'Karn Liberated'))
  }
}

# convert play/draw input to 0/1
pd_converter <- function(pd) {
  if (pd == 'play') {
    return(0)
  } else {
    return(1)
  }
}

# return the count of a given card in the hand
count_cards <- function(card_name, hand_df) {
  if (card_name %in% hand_df$name) {
    return(hand_df$count[hand_df$name == card_name])
  } else {
    return(0)
  }
}

# count the number of unique tron lands in hand
count_tron <- function(card_nums) {
  # relies on index position of the tron lands in card_nums
  mine <- card_nums[6] > 0
  pplant <- card_nums[7] > 0
  tower <- card_nums[8] > 0
  mine + pplant + tower
}

# format the hand to pass into RF model
format_hand <- function(hand_df, mull_count, play_draw, ref_df) {
  
  vars <- c('Ancient Stirrings', 'Expedition Map', 'Forest', 'Relic of Progenitus',
            'Sylvan Scrying', 'Urzas Mine', 'Urzas Power Plant', 'Urzas Tower')
  card_nums <- sapply(vars, function(card_name){
    count_cards(card_name, hand_df)
  })
  
  # engineering additional features  
  chromatic_count <- count_cards('Chromatic Star', hand_df) + 
    count_cards('Chromatic Sphere', hand_df)
  other_lands <- count_cards('Ghost Quarter', hand_df) + 
    count_cards('Sanctum of Ugin', hand_df)
  unique_tron <- count_tron(card_nums)
  tron_map_count <- unique_tron + (card_nums[2] > 0)
  total_lands <- sum(card_nums[6:8]) + card_nums[3] + other_lands
  
  ref_df[1,] <- c(
    card_nums,
    7 - mull_count,
    pd_converter(play_draw),
    chromatic_count,
    other_lands,
    unique_tron,
    tron_map_count,
    total_lands,
    0
  )
  return(ref_df)
}

# run model, considering mulligans to return the best hand
analyze_hand <- function(opener, mull_count, play_draw) {
  all_hands <- combn(opener, 7 - mull_count)
  predictions <- sapply(1:ncol(all_hands), function(i){
    hand_df <- data.frame(table(all_hands[,i]))
    names(hand_df) <- c('name', 'count')
    model_input <- format_hand(hand_df, mull_count, play_draw, ref_df)
    predict(model, model_input[1,])
  })
  best_turn <- min(predictions)
  best_hand <- all_hands[,which.min(predictions)]
  return(c(best_turn, best_hand))
}

# render the images for cards in a hand
render_hand <- function(hand) {
  lapply(sort(hand), function(card_name){
    url <- paste("<img src='https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=",
                 as.character(cardlist$gatherer_id[cardlist$name == card_name]),
                 "&type=card' height='150px'>", sep = '')
    column(width = 2, HTML(url))
  })
}

# compare current hand to next mulligan
qc_hand <- function(next_handsize, pd, predicted_turn) {
  sample <- hand_comps %>%
    filter(handsize == next_handsize) %>%
    filter(play_draw == pd) %>%
    filter(pred > predicted_turn)
  return(nrow(sample)/5000 * 100)
}

ui <- dashboardPage(
  skin = 'green',
  dashboardHeader(title = 'MtG Divination - Tron'),
  dashboardSidebar(
    
    uiOutput(outputId = 'subtitle'),
    tags$head(tags$style(HTML("
                            #subtitle {
                              font-size: 20px; 
                            }
                            "))),
    
    # tabs to fill in counts for each card type
    sidebarMenu(
      menuItem('Creatures', tabName = 'Creatures'),
      menuItem('Planeswalkers', tabName = 'Planeswalkers'),
      menuItem('Sorceries', tabName = 'Sorceries'),
      menuItem('Artifacts', tabName = 'Artifacts'),
      menuItem('Lands', tabName = 'Lands')
    ),
    
    # input for hand size
    numericInput(inputId = 'mulligan',
                 label = 'Mulligans taken',
                 value = 0,
                 min = 0,
                 max = 4,
                 width = '140px'),
    
    # input for play/draw
    radioButtons(inputId = 'play_draw',
                 label = 'On the play or on the draw?',
                 choices = c('play', 'draw'),
                 inline = TRUE),
           
    actionButton(inputId = 'go',
                 label = 'Predict Outcome'),
    
    sidebarMenu(
      id = 'output_display',
      menuItem('Results', tabName = 'Results')
    )
    
  ),
  
  dashboardBody(
    tags$head( 
      tags$style(HTML(".content { font-size: 18px; }"))
      ),
    tags$head( 
      tags$style(HTML(".main-sidebar { font-size: 15px; }"))
      ),

    tabItems(
      tabItem(tabName = 'Creatures',
              fluidRow( tabPanel('Creatures', uiOutput('creature_cards')) ),
              fluidRow( tabPanel('Creatures', uiOutput('creature_inputs')) )
              ),
      tabItem(tabName = 'Planeswalkers',
              fluidRow( tabPanel('Planeswalkers', uiOutput('planeswalker_cards')) ),
              fluidRow( tabPanel('Planeswalkers', uiOutput('planeswalker_inputs')) )
              ),
      tabItem(tabName = 'Sorceries',
              fluidRow( tabPanel('Sorceries', uiOutput('sorcery_cards')) ),
              fluidRow( tabPanel('Sorceries', uiOutput('sorcery_inputs')) )
              ),
      tabItem(tabName = 'Artifacts',
              fluidRow( tabPanel('Artifacts', uiOutput('artifact_cards')) ),
              fluidRow( tabPanel('Artifacts', uiOutput('artifact_inputs')) )
              ),
      tabItem(tabName = 'Lands',
              fluidRow( tabPanel('Lands', uiOutput('land_cards')) ),
              fluidRow( tabPanel('Lands', uiOutput('land_inputs')) )
              ),
      tabItem(tabName = 'Results',
              fluidRow( tabPanel('Results', 
                                 column(12,textOutput(outputId = 'opener_header'))
                                 ) ),
              #render 7 card hand
              fluidRow( tabPanel('Results', uiOutput('opener_cards')) ),
              br(),
              fluidRow( tabPanel('Results', 
                                 column(12, textOutput(outputId = 'best_header')) 
                                 ) ),
              #render best n card hand
              fluidRow( tabPanel('Results', uiOutput('best_cards')) ),
              br(),
              #print results from model and suggestion
              fluidRow( tabPanel('Results', 
                                 column(12, uiOutput(outputId = 'prediction')) 
                                 ) )
              )
    )
  )
)



server <- function(input, output, session) {
  
  output$subtitle <- renderUI({ HTML('&ensp; Input your 7 card hand') })
  
  output$creature_cards <- renderUI({ render_imgs('creature') })
  output$planeswalker_cards <- renderUI({ render_imgs('planeswalker') })
  output$sorcery_cards <- renderUI({ render_imgs('sorcery') })
  output$artifact_cards <- renderUI({ render_imgs('artifact') })
  output$land_cards <- renderUI({ render_imgs('land') })
  
  output$creature_inputs <- renderUI({ render_inputs('creature') })
  output$planeswalker_inputs <- renderUI({ render_inputs('planeswalker') })
  output$sorcery_inputs <- renderUI({ render_inputs('sorcery') })
  output$artifact_inputs <- renderUI({ render_inputs('artifact') })
  output$land_inputs <- renderUI({ render_inputs('land') })
  
  output$opener_header <- renderText({ 'Your opening 7 cards:' })
  output$best_header <- renderText({ 'Your best hand:' })
  
  # take in user input and pass hand through the model
  count_table <- eventReactive(input$go, { count_hand(input) })
  opener <- eventReactive(input$go, { get_opener(count_table()) } )
  model_output <- eventReactive(input$go, {analyze_hand(opener(), input$mulligan, input$play_draw) })
  
  # render the images for the opening 7 cards and best mulligan hand
  output$opener_cards <- renderUI({ render_hand(opener()) })
  output$best_cards <- renderUI({ render_hand(model_output()[2:length(model_output())]) })
  
  # output the predicted results
  output$prediction <- renderUI({
    
    # compare quality of current hand to next mullgain
    next_handsize <- isolate({ 6 - input$mulligan })
    quality <- isolate({
      qc_hand(next_handsize, pd_converter(input$play_draw), as.numeric(model_output()[1]))
      })
    
    # display results
    line1 <- paste('Predicted turns for Tron: ', 
                   round(as.numeric(model_output()[1]), 2),
                   sep = '')
    line2 <- paste('This is better than ', 
                   quality, 
                   '% of ', 
                   next_handsize, 
                   ' card hands.',
                   sep = '')
    HTML(paste(line1, '<br>', line2))
  })
  
  # redirect to results tab when model is run
  observeEvent(input$go, { 
    updateTabsetPanel(session, 'output_display', selected = 'Results') 
    })
    
}

shinyApp(ui = ui, server = server)
