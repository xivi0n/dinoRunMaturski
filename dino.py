import pygame
import time
import random
import numpy 

from player import *
from drawing import *
from objects import *

import pickle
import matplotlib.pyplot as plt
import neural_network as NN
import genetic_algorithm as GA

population_size = 50
num_parents_mating = int(population_size*0.25)
num_generations = 2000
mutation_percent = 10

best_scores = []
dead_obj_count = {
        0: [0,0,0,0], #cactus w: 1 2 3 4
        1: [0,0]      #bird   h: L H  
    }

def prepare_quit(pop_weights_mat,score):
    global best_scores
    best_scores.append(score)
    normal_values = []
    for sc in best_scores:
        scaledValue = 1.0*(sc - min(best_scores)) / (max(best_scores) - min(best_scores))
        normal_values.append(scaledValue)

    best_scores = normal_values
    if best_scores!=[]:
        f = open("results/"+"weights_"+str(num_generations)+"_iterations_"+str(mutation_percent)+"%_mutation.pkl","wb")
        pickle.dump(pop_weights_mat, f)
        f.close()

        print(best_scores)
        print("With a best score %d on %d generation"%(max(best_scores),best_scores.index(max(best_scores))))

        print (dead_obj_count)
        
        plt.plot(best_scores, linewidth=5, color="black")
        plt.xlabel("Generations", fontsize=20)
        plt.ylabel("Fitness", fontsize=20)
        plt.xticks(numpy.arange(0, len(best_scores)+1, 10), fontsize=15)
        plt.yticks(numpy.arange(0, max(best_scores), 50), fontsize=15)
        plt.show()

def gameStart():
    gameStart = False
    while not gameStart:
        message_display(str("Press S to START"),(450),(150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                if event.key == pygame.K_s:
                    gameStart = True

        pygame.display.update()
        clock.tick(CLOCK_SPEED)

def handle_input(player):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not player.crouch:
                        return 1
                        player.startJump()

                if event.key == pygame.K_DOWN:
                    if not player.jump:
                        return -1
                        player.crouch(True)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                if event.key == pygame.K_UP:
                    pass
                
                if event.key == pygame.K_DOWN:
                    return 0
                    player.crouch(False)

    if player.jump:
        return 1
        
    if player.crouch:
        return -1
    
    return 0

def game_loop(players,generation,pop_weights_mat):
    score = 0
    gameExit = False
    dead_players_idx = []
    dead_players_obj = []
    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                prepare_quit(pop_weights_mat,score)
                pygame.quit()
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    prepare_quit(pop_weights_mat,score)
                    pygame.quit()
                    quit()

                if event.key == pygame.K_s:
                    gameStart()

        score += 1
        drawBG()

        for i in range(len(players)):
            
            if not i in dead_players_idx:
                check, obj_idx = players[i].collide(objects,display_width)
                if check:
                    if len(players)-len(dead_players_idx)==1:
                        dead_players_obj.append([objects[obj_idx][1],objects[obj_idx][2]])
                    dead_players_idx.append(i)
                else:
                    #k = random.randint(-1,1)
                    obj = objects[closest(players[i].x)]
                    data_input = [obj[1],obj[2],obj[0],speed] #speed,obj[0],obj[1],obj[2]
                    curr_sol_mat = pop_weights_mat[i,:]
                    k = NN.predict_label(curr_sol_mat, data_input,activation="relu") #sigmoid/relu
                    drawName,iSprite = players[i].move(k,sprites)
                    draw(sprites[drawName][iSprite],players[i].x,players[i].y)
            
        #         if score>400:
        #             print(players[i].y,"move:",k,"jump/crouch:",players[i].jump,players[i].crouch,end=' ')
        # if score>400:
        #     print()

        if not len(players)-len(dead_players_idx):
            gameExit = True

        drawObj(score)

        message_display(str("Score: %d"%(score)),(50),(50))
        message_display(str("Generation: %d"%(generation)),(50),(68))
        message_display(str("Alive: %d"%(len(players)-len(dead_players_idx))),(50),(86))
        

        pygame.display.update()
        clock.tick(CLOCK_SPEED)

    return dead_players_idx,dead_players_obj

        

############################
# for playing
#     player = Player(50,baseH)
#     currSprite = sprites["run"][0]
#     draw(currSprite,player.x,player.y)
#     message_display("Press UP",(display_width-150),(50))
#     pygame.display.update()
#     gameStart()
#     score = 0
# ############################
    
#     while not gameExit:

#         # for playing
#         k = handle_input(player)
#         #
#         drawName,iSprite = player.move(k,sprites)

#         drawBG()
#         draw(sprites[drawName][iSprite],player.x,player.y)
#         drawObj(score)

#         score += 1
        
#         message_display(str("Score: %d"%(score)),(display_width-150),(50))

#         pygame.display.update()
#         clock.tick(CLOCK_SPEED)

#         if player.collide(objects,display_width):
#             print(score)
#             player.reset()
#             resetObjects()
#             game_loop()

def main():
    global best_scores, dead_obj_count
    loadAssets()
    
    init_pop_weights = []
    HL1_neurons = 20
    HL2_neurons = 10
    output_neurons = 3
    input_neurons = 4

    for i in range(population_size):
        input_HL1_weights = numpy.random.uniform(low=-1.0, high=1.0, 
                                             size=(input_neurons, HL1_neurons))
        HL1_HL2_weights = numpy.random.uniform(low=-1.0, high=1.0, 
                                             size=(HL1_neurons, HL2_neurons)) 
        HL2_output_weights = numpy.random.uniform(low=-1.0, high=1.0, 
                                              size=(HL2_neurons, output_neurons))

        init_pop_weights.append(numpy.array([input_HL1_weights, 
                                                HL1_HL2_weights,
                                                HL2_output_weights])) 


    pop_weights_mat = numpy.array(init_pop_weights)
    pop_weights_vector = GA.mat_to_vector(pop_weights_mat)

    players = [Player(50,baseH) for i in range(population_size)]
    
    for generation in range(num_generations):
        print("Generation: %d"%(generation))

        resetObjects()
        predefineObjects(distance)
        [player.reset() for player in players]

        pop_weights_mat = GA.vector_to_mat(pop_weights_vector, pop_weights_mat)
        player_order, dead_obj = game_loop(players,generation,pop_weights_mat)

        for obj in dead_obj:
            if obj[0] == 0:
                dead_obj_count[0][obj[1]]+=1
            elif obj[0] == 1:
                dead_obj_count[1][obj[1]%2]+=1

        fitness = numpy.empty(len(player_order))
        for i in player_order:
            fitness[i] = players[i].score

        #print(fitness)
        parents = GA.select_mating_pool(pop_weights_vector, fitness.copy(), num_parents_mating)
        print("Parents selected")

        offspring_crossover = GA.crossover(parents,
                                       offspring_size=(pop_weights_vector.shape[0]-parents.shape[0], pop_weights_vector.shape[1]))
        print("Crossover completed")

        offspring_mutation = GA.mutation(offspring_crossover, 
                                     mutation_percent=mutation_percent)
        print("Mutation completed")

        pop_weights_vector[0:parents.shape[0], :] = parents
        pop_weights_vector[parents.shape[0]:, :] = offspring_mutation

        best_score = players[player_order[-1]].score
        best_scores.append(best_score)
        print("Best score: %d\n" %(best_score))
    
    prepare_quit(pop_weights_mat)

    gameStart()

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()
