import os
import global_variables
import sys
import string
import pygame
import datetime
import math
import company
import primitives
import gui_components

import random
import time






class gui():
    """
    This class holds all the top-level gui stuff, such as functions to distribute clicks and the commandbox buttons on the right side and such
    """
    def __init__(self,right_side_surface, message_surface, action_surface, solar_system_object):
        """
        Here the commandbox is started initialized. In addition all the other GUI elements is started up, to keep it at one place
        """
        
        
        # defining 
        command_box_left = right_side_surface.get_offset()[0]
        command_width = right_side_surface.get_size()[0]
        infobox_top = 0
        command_top = 70
        subcommand_top = 470
        
        
        self.action_rect = pygame.Rect(0,0, action_surface.get_size()[0], action_surface.get_size()[1])
        self.infobox_rect = pygame.Rect(command_box_left, infobox_top, command_width, command_top)
        self.command_rect =  pygame.Rect(command_box_left, command_top, command_width, subcommand_top-command_top)
        self.subcommand_rect = pygame.Rect(command_box_left, subcommand_top, command_width, global_variables.window_size[1] -subcommand_top)

        self.action_surface = action_surface
        self.infobox_surface = right_side_surface.subsurface(pygame.Rect(0, infobox_top, command_width, command_top))
        self.command_surface =  right_side_surface.subsurface(pygame.Rect(0, command_top, command_width, subcommand_top-command_top))
        self.subcommand_surface = right_side_surface.subsurface(pygame.Rect(0, subcommand_top, command_width, global_variables.window_size[1] -subcommand_top))


        self.solar_system_object_link = solar_system_object
        
        
        self.active_window = None
        
        self.all_windows = {}
        
        self.all_windows["Messages"] = message_bar(solar_system_object, action_surface, message_surface)
        self.all_windows["Company menu"] = company_window(solar_system_object, action_surface)
        self.all_windows["Trade menu"] = trade_window(solar_system_object, action_surface)
        self.all_windows["Base overview"] = base_window(solar_system_object, action_surface)
        self.all_windows["Map overlays"] = overlay_window(solar_system_object, action_surface)
        self.all_windows["Planet shortcuts"] = planet_jump_window(solar_system_object, action_surface)
        self.all_windows["Navigation"] = navigation_window(solar_system_object, action_surface)
        self.all_windows["File menu"] = file_window(solar_system_object, action_surface)
        self.all_windows["Technology"] = tech_window(solar_system_object, action_surface)
        
        self.all_windows["base_population_info"] = base_population_info(solar_system_object, action_surface)
        self.all_windows["base_list_of_companies"] = base_list_of_companies(solar_system_object, action_surface)
        self.all_windows["base_list_of_firms"] = base_list_of_firms(solar_system_object, action_surface)
        self.all_windows["base_and_firm_market_window"] = base_and_firm_market_window(solar_system_object, action_surface)
        self.all_windows["base_build_menu"] = base_build_menu(solar_system_object, action_surface)
        self.all_windows["company_ownership_info"] = company_ownership_info(solar_system_object, action_surface)
        self.all_windows["company_financial_info"] = company_financial_info(solar_system_object, action_surface)
        self.all_windows["company_list_of_firms"] = company_list_of_firms(solar_system_object, action_surface)
        self.all_windows["firm_trade_partners_info"] = firm_trade_partners_info(solar_system_object, action_surface)
        self.all_windows["firm_process_info"] = firm_process_info(solar_system_object, action_surface)
        self.all_windows["firm_process_info"] = firm_process_info(solar_system_object, action_surface)
        self.all_windows["construct_base_menu"] = construct_base_menu(solar_system_object, action_surface)
        
        self.create_infobox()
        self.create_commandbox()
        self.create_subcommandbox()

        
        
    
    def receive_click(self,event):
        """
        Function that distributes clicks where necessary
        """

        #Checking where the click is located
        if self.command_rect.collidepoint(event.pos) == 1:
            for button in self.command_buttons.values():
                if button.rect.collidepoint((event.pos[0] - global_variables.window_size[0] + self.command_rect[2], event.pos[1] - self.command_rect[1])) == 1:
                    button.activate(None)
                    return 

        if self.subcommand_rect.collidepoint(event.pos) == 1:
            for button in self.subcommand_buttons.values():
                if button.rect.collidepoint((event.pos[0] - global_variables.window_size[0] + self.subcommand_rect[2], event.pos[1] - self.subcommand_rect[1])) == 1:
                    button.activate(None)
                    return 


        elif self.action_rect.collidepoint(event.pos) == 1:
            if self.active_window is not None:
                if self.active_window.rect.collidepoint(event.pos) == 1:
                    return_value = self.active_window.receive_click(event)
                    if return_value is not None:
                        if return_value == "clear":
                            self.clear_screen()
                        elif return_value == "new base":
                            self.solar_system_object_link.display_mode = "planetary"
                            self.solar_system_object_link.build_base_mode = True
                            self.clear_screen()
                            text = global_variables.standard_font.render("Choose position of new base:",True,(150,150,150))
                            self.action_surface.blit(text, (global_variables.window_size[0] / 2 - text.get_width()/2, 400))
                            self.active_window = self.all_windows["construct_base_menu"]
                            pygame.display.flip()
                        else:
                            print "should zoom to " + str(return_value)
                    return

        self.click_in_action_window(event)

        
        #updating the infobox in any case
        self.create_infobox()
        self.all_windows["Messages"].create()
        pygame.display.flip()


        

    def clear_screen(self):
        """
        Function that takes care of clearing screen, by drawing whatever planet or solar system or base window that is supposed
        to be on it, thus overwriting what gui-box might be there
        """
        self.active_window = None
        sol = self.solar_system_object_link
        if sol.display_mode == "solar_system":
            self.action_surface.blit(sol.draw_solar_system(zoom_level=sol.solar_system_zoom,date_variable=sol.current_date,center_object=sol.current_planet.planet_name),(0,0))
        elif sol.display_mode == "planetary":
            self.action_surface.blit(sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling),(0,0))                        
        elif sol.display_mode == "base":
            self.going_to_base_mode_event(sol.current_planet.current_base)
        elif sol.display_mode == "firm":
            self.going_to_firm_window_event(sol.firm_selected)
        elif sol.display_mode == "company":
            self.going_to_company_window_event(sol.company_selected)
        elif sol.display_mode in ["techtree"]:
            pass
        else:
            print "error. The mode: " + sol.display_mode +" is unknown"
        
        self.create_subcommandbox()
        pygame.display.flip()



    def zoom_in(self,event):
        self.clear_screen()
        sol = self.solar_system_object_link
        if sol.display_mode == "solar_system":
            sol.solar_system_zoom = sol.solar_system_zoom * 2
            surface = sol.draw_solar_system(zoom_level=sol.solar_system_zoom,date_variable=sol.current_date,center_object=sol.current_planet.planet_name)
            if surface == "planetary_mode":
                sol.solar_system_zoom = sol.solar_system_zoom / 2
                sol.display_mode = "planetary"
                sol.current_planet.load_for_drawing()
                surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)
        elif sol.display_mode == "planetary":
            if sol.current_planet.projection_scaling < 720:
                sol.current_planet.projection_scaling = sol.current_planet.projection_scaling * 2
                surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)                        
            else:
                if sol.current_planet.current_base is not None: #if a base is selected on this planet, we'll zoom in on it
                    sol.display_mode = "base"
                    self.going_to_base_mode_event(sol.current_planet.current_base)
                    return
                else:
                    return
        elif sol.display_mode in ["base","firm","company"]:
            return
        elif sol.display_mode in ["techtree"]:
            surface = sol.technology_tree.zoom("in")
        else:
            print "error. The mode: " + sol.display_mode +" is unknown"
            return

        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()

    
        
    def zoom_out(self,event):
        self.clear_screen()
        sol = self.solar_system_object_link
        if sol.display_mode == "solar_system":
            if sol.solar_system_zoom >= 2:
                sol.solar_system_zoom = sol.solar_system_zoom / 2
                surface = sol.draw_solar_system(zoom_level=sol.solar_system_zoom,date_variable=sol.current_date,center_object=sol.current_planet.planet_name)
            else:
                return
        
        elif sol.display_mode == "planetary":
            if sol.current_planet.projection_scaling >= 90:
                sol.current_planet.projection_scaling = sol.current_planet.projection_scaling / 2
                surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)
            else:
                sol.current_planet.unload_from_drawing()
                sol.display_mode = "solar_system" 
                surface = sol.draw_solar_system(zoom_level=sol.solar_system_zoom,date_variable=datetime.date(2102,1,22),center_object=sol.current_planet.planet_name)
        elif sol.display_mode in ["firm","company","base"]:
            surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)
            sol.display_mode = "planetary"
            self.create_subcommandbox()
        elif sol.display_mode in ["techtree"]:
            surface = sol.technology_tree.zoom("out")
            
        else:
            print "error. The mode: " + sol.display_mode +" is unknown"
            return
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()
                

    
    def click_in_action_window(self,event):
        sol = self.solar_system_object_link
        position = event.pos
        button = event.button
        click_spot = pygame.Rect(position[0]-3,position[1]-3,6,6)
        if sol.display_mode == "solar_system":
            
            collision_test_result = click_spot.collidedict(sol.areas_of_interest)
            
            if collision_test_result != None:
                sol.current_planet = sol.planets[collision_test_result[1]]
                surface = sol.draw_solar_system(zoom_level=sol.solar_system_zoom,date_variable=sol.current_date,center_object=sol.current_planet.planet_name)
                if surface == "planetary_mode":
                    manager.emit("going_to_planetary_mode_event",sol.current_planet)
                    sol.solar_system_zoom = 200000000 / sol.current_planet.planet_diameter_km  
                    sol.display_mode = "planetary"
                    sol.current_planet.load_for_drawing()
                    surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)
                self.action_surface.blit(surface,(0,0))
                pygame.display.flip()
        
        elif sol.display_mode == "planetary":
        
            if sol.build_base_mode: #if we are in the special build base mode, there should be a base creation instead.
                sphere_coordinates = sol.current_planet.check_base_position(position)
                
                if isinstance(sphere_coordinates, tuple): #if the selection was correctly verified by check_base_position we send it back to the GUI for further processing
                    sol.build_base_mode = False
                    self.all_windows["construct_base_menu"].new_base_ask_for_name(sphere_coordinates)
                return
            
            else: #if we are not in build_base_mode we work as normally
                areas_of_interest = sol.current_planet.areas_of_interest[(sol.current_planet.northern_inclination,sol.current_planet.eastern_inclination,sol.current_planet.projection_scaling)]
                collision_test_result = click_spot.collidedict(areas_of_interest)
                if collision_test_result != None:
                    current_base = sol.current_planet.bases[collision_test_result[1]]
                    #print "current_base " + str(current_base)
                    sol.current_planet.current_base = current_base
                    if button == 1:
                        surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)
                    if button == 3:
                        self.going_to_base_mode_event(current_base)
                        
                        return
                else:
                    return

            self.action_surface.blit(surface,(0,0))
            pygame.display.flip()

        
        elif sol.display_mode in ["techtree"]:
            surface = sol.technology_tree.receive_click(event)
            self.action_surface.blit(surface,(0,0))
            pygame.display.flip()
        
        elif sol.display_mode in ["company","firm","base"]:
            pass            
        else:
            print "error. The mode: " + sol.display_mode +" is unknown"                

            
            
            
    
    def go_left(self,event):
        self.clear_screen()
        sol = self.solar_system_object_link
        if sol.display_mode == "planetary":
            sol.current_planet.eastern_inclination = sol.current_planet.eastern_inclination - 30
            if sol.current_planet.eastern_inclination <= -180:
                sol.current_planet.eastern_inclination = sol.current_planet.eastern_inclination + 360
            surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)
        elif sol.display_mode == "techtree":
            surface = sol.technology_tree.move("left")
        else:
            return
        
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()
        
    def go_right(self,event):
        self.clear_screen()
        sol = self.solar_system_object_link
        if sol.display_mode == "planetary":
            sol.current_planet.eastern_inclination = sol.current_planet.eastern_inclination + 30
            if sol.current_planet.eastern_inclination > 180:
                sol.current_planet.eastern_inclination = sol.current_planet.eastern_inclination - 360
            
            surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)
        elif sol.display_mode == "techtree":
            surface = sol.technology_tree.move("right")
        else:
            return
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()

        
    def go_down(self,event):
        self.clear_screen()
        sol = self.solar_system_object_link
        if sol.display_mode == "planetary":
            if sol.current_planet.northern_inclination > -90:
                sol.current_planet.northern_inclination = sol.current_planet.northern_inclination - 30
                surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)
            else:
                return
        elif sol.display_mode == "techtree":
            surface = sol.technology_tree.move("down")
        else:
            return
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()


    
    def go_up(self,event):
        self.clear_screen()
        sol = self.solar_system_object_link
        if sol.display_mode == "planetary":
            if sol.current_planet.northern_inclination < 90:
                sol.current_planet.northern_inclination = sol.current_planet.northern_inclination + 30
                surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)
            else:
                return
        elif sol.display_mode == "techtree":
            surface = sol.technology_tree.move("up")
        else:
            return
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()


        
    

#            print "error. The mode: " + sol.display_mode +" does not accept a/z input"


        


    def going_to_company_window_event(self,company_selected):
        sol = self.solar_system_object_link
#        company_selected = event.data
#        mode_before_change = sol.display_mode
        sol.display_mode = "company"
        surface = company_selected.draw_company_window()
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()

    def going_to_firm_window_event(self,firm_selected):
        sol = self.solar_system_object_link
        sol.display_mode = "firm"
        surface = firm_selected.draw_firm_window()
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()
        
    def going_to_base_mode_event(self,base_selected):
        sol = self.solar_system_object_link
#        mode_before_change = sol.display_mode
        sol.current_planet.current_base = base_selected
        sol.current_planet = base_selected.home_planet
        sol.display_mode = "base"
        surface = base_selected.draw_base_window()
        self.create_subcommandbox()
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()
















        
#


    def create_infobox(self):
        self.infobox_surface.fill((150,150,150))
        
        # creating the date string
        date_string = str(self.solar_system_object_link.current_date)
        rendered_date_string = global_variables.standard_font.render(date_string,True,(0,0,0))
        self.infobox_surface.blit(rendered_date_string, (10,10))

        # creating the env string
        if self.solar_system_object_link.display_mode == "solar_system":
            env_string = "Solar system -" + string.capitalize(self.solar_system_object_link.current_planet.planet_name)
        elif self.solar_system_object_link.display_mode == "planetary":
            if self.solar_system_object_link.current_planet.current_base == None:
                env_string = self.solar_system_object_link.current_planet.planet_name
            else:
                env_string = self.solar_system_object_link.current_planet.planet_name + " - " + self.solar_system_object_link.current_planet.current_base.name 
        elif self.solar_system_object_link.display_mode == "planetary":
            env_string = self.solar_system_object_link.current_planet.current_base.name
        elif self.solar_system_object_link.display_mode == "company":
            env_string = self.solar_system_object_link.company_selected.name
        elif self.solar_system_object_link.display_mode == "firm":
            env_string = self.solar_system_object_link.firm_selected.name
        elif self.solar_system_object_link.display_mode == "base":
            env_string = self.solar_system_object_link.current_planet.current_base.name
        elif self.solar_system_object_link.display_mode == "techtree":
            env_string = "technology tree"
        else:
            env_string = ""
            if self.solar_system_object_link.message_printing["debugging"]:
                print_dict = {"text":"DEBUGGING: unknown display mode passed to infobox","type":"debugging"}
                self.solar_system_object_link.messages.append(print_dict)
        rendered_env_string = global_variables.standard_font.render(env_string,True,(0,0,0))
        self.infobox_surface.blit(rendered_env_string, (10,30))

        
        #creating the capital string
        if self.solar_system_object_link.current_player is not None:
            capital_string = str(int(self.solar_system_object_link.current_player.capital))
            rendered_capital_string = global_variables.standard_font.render(capital_string,True,(0,0,0))
            self.infobox_surface.blit(rendered_capital_string, (10,50))
        
        
    
    def commandbox_button_activate(self,label, function_parameter):
        """
        Function that decides what to do if a commandbox button is pressed
        """
        if label == "Technology":
            if self.solar_system_object_link.display_mode == "techtree":
                self.solar_system_object_link.display_mode = self.all_windows["Technology"].display_mode_before
                self.clear_screen()
                return
            else:
                self.all_windows["Technology"].display_mode_before = self.solar_system_object_link.display_mode
                
            
        
        self.clear_screen()
        self.active_window = self.all_windows[label]
        self.all_windows[function_parameter].create()
        
    
    def create_commandbox(self):    
        """
        Creates the right-side menu command box
        """
        self.command_surface.fill((150,150,150))
#        pygame.draw.rect(self.command_surface, (150,150,150), self.command_rect)
        
        labels = ["Navigation","Map overlays","Planet shortcuts","Company menu","Base overview","Technology","Trade menu","File menu"]
        self.command_buttons = {}
        for i, label in enumerate(labels):
            self.command_buttons[label] = gui_components.button(label, 
                                                                self.command_surface,
                                                                self.commandbox_button_activate, 
                                                                function_parameter = label, 
                                                                fixed_size = (self.command_rect[2]-20,35), topleft = (10, i * 40 + 10))

    
    
    def subcommandbox_button_activate(self, nicelabel, label):
        self.all_windows[label].create()
        self.active_window = self.all_windows[label]

    def create_subcommandbox(self):    
        """
        Creates the right-side menu lower subcommand box
        """
        self.subcommand_surface.fill((150,150,150))
        self.subcommand_buttons = {}
#        pygame.draw.rect(self.subcommand_surface, (150,150,150), self.subcommand_rect)

        if self.solar_system_object_link.display_mode == "base":
            self.buttonlinks = ["base_population_info","base_list_of_companies","base_list_of_firms","base_and_firm_market_window","base_build_menu"]
            self.buttonnicenames = ["Population","Companies","Firms","Market","Build"]
        elif self.solar_system_object_link.display_mode == "firm":
            self.buttonlinks = ["firm_process_info","base_and_firm_market_window","firm_trade_partners_info"]
            self.buttonnicenames = ["Production","Market","Trade partners"]
        elif self.solar_system_object_link.display_mode == "company":
            self.buttonlinks = ["company_ownership_info","company_financial_info","company_list_of_firms"]
            self.buttonnicenames = ["Ownership info","Financial info","Owned firms"]

        else:
            
            pygame.display.flip()
            return
        
        self.subcommand_buttons = {}
        for i, label in enumerate(self.buttonlinks):
            self.subcommand_buttons[label] = gui_components.button(self.buttonnicenames[i], self.subcommand_surface,
                                                                self.subcommandbox_button_activate, function_parameter = label, 
                                                                fixed_size = (self.subcommand_surface.get_width()-20,35), 
                                                                topleft = (10, i * 40 + 10))
        
        pygame.display.flip()
        






class infobox_window():
    """
    The infobox window. Always visible and shows time and location - ie "solarsystem, centered on earth",
    "Frankfurt" etc. It also shows internet-browser style backward and forward buttons.
    """
    def __init__(self,solar_system_object,commandbox):
        self.solar_system_object_link = solar_system_object
        self.size = (400,40)
        self.topleft = (global_variables.window_size[0]/2 - self.size[0]/2,0)
        self.data = self.update_data()
        self.history = []
        self.has_been_history = []
        self.history_button_size = (30,30)
        self.current_event = Signals.Event("going_to_planetary_mode_event",self.solar_system_object_link.current_planet)
        self.protect_has_been_history = False  #Without this variable has_been_history would be deleted even when going steps forward
        self.create_infobox(self.renderer)
        
    
    def forwardbutton_callback(self):
        if len(self.has_been_history) > 0: 
            signal_to_emit = self.has_been_history.pop()
            
            self.protect_has_been_history = True
            if signal_to_emit.signal == "going_to_solar_system_mode_event":
                self.solar_system_object_link.current_planet.projection_scaling = 45
                self.solar_system_object_link.display_mode = "planetary"
                self.manager.emit("zoom_out",None)
            elif signal_to_emit.signal == "going_to_planetary_mode_event":
                self.manager.emit("center_on",signal_to_emit.data.name)
            else:
                self.manager.emit(signal_to_emit.signal,signal_to_emit.data)
            self.protect_has_been_history = False
        
        else:
            raise Exception("The forward button was pressed but it should not have been set to sensitive")

        if len(self.has_been_history) < 1:
            self.forwardbutton.sensitive = False

        
    def backbutton_callback(self):
        
        if len(self.history) > 0:
            self.has_been_history.append(self.current_event)

            signal_to_emit = self.history.pop()
            self.protect_has_been_history = True
            if signal_to_emit.signal == "going_to_solar_system_mode_event":
                #print "going to solar system mode"
                self.solar_system_object_link.current_planet.projection_scaling = 45
                self.solar_system_object_link.display_mode = "planetary"
                self.manager.emit("zoom_out",None)
            elif signal_to_emit.signal == "going_to_planetary_mode_event":
                self.manager.emit("center_on",signal_to_emit.data.name)
            else:
                self.manager.emit(signal_to_emit.signal,signal_to_emit.data)
            self.protect_has_been_history = False
            
            try: self.forwardbutton.sensitive
            except: pass
            else:
                self.forwardbutton.sensitive = True
            
            self.history.pop()
        else:
            raise Exception("The back button was pressed but it should not have been set to sensitive")

        if len(self.history) < 1:
            try: self.backbutton.sensitive
            except: pass
            else:
                self.backbutton.sensitive = False
        
        
    def create_infobox(self,renderer):
        """
        The creation function. Doesn't return anything, but saves self.window variable and renders using the self.renderer. 
        """
        info_label = Label(self.data)
        info_label.multiline = True
        self.window = VFrame()
        self.window.set_opacity(100)
        self.window.border = BORDER_NONE
        self.window.add_child(info_label)
        self.window.topleft = self.topleft
        self.window.minsize = self.size
        self.window.depth = 1
        renderer.add_widget(self.window)
        
        
        #Drawing a button with an arrow
        blank_surface = pygame.Surface(self.history_button_size)
        blank_surface.fill((234,228,223))
        pygame.draw.line(blank_surface,(155,155,155),(5,13),(30,13))
        pygame.draw.line(blank_surface,(155,155,155),(5,16),(30,16))
        pygame.draw.line(blank_surface,(155,155,155),(0,15),(5,10))
        pygame.draw.line(blank_surface,(155,155,155),(0,15),(5,20))
        pygame.draw.line(blank_surface,(155,155,155),(5,10),(5,13))
        pygame.draw.line(blank_surface,(155,155,155),(5,20),(5,16))
        pygame.draw.line(blank_surface,(155,155,155),(30,13),(30,16))

        flipped_blank_surface = pygame.transform.flip(blank_surface,True,False)
        
        self.backbutton = ImageButton(blank_surface)
        self.forwardbutton = ImageButton(flipped_blank_surface)
        self.backbutton.set_opacity(100)
        self.forwardbutton.set_opacity(100)
        self.forwardbutton.topleft = (self.topleft[0] + self.size[0] + 5, self.topleft[1])
        self.backbutton.topleft = (self.topleft[0] - self.history_button_size[0] - 15 , self.topleft[1])
        if len(self.history) < 1:
            self.backbutton.sensitive = False
        if len(self.has_been_history) < 1:
            self.forwardbutton.sensitive = False

        
        self.backbutton.connect_signal(Constants.SIG_CLICKED,self.backbutton_callback)
        self.forwardbutton.connect_signal(Constants.SIG_CLICKED,self.forwardbutton_callback)

        self.backbutton.depth = 1
        self.forwardbutton.depth = 1

        
        self.renderer.add_widget(self.backbutton,self.forwardbutton)
        
        
    def exit(self):
        try: self.window
        except: pass
        else:
            self.window.destroy()
            del self.window
        try: self.backbutton
        except: pass
        else:
            self.backbutton.destroy()
            del self.backbutton
        try: self.forwardbutton
        except: pass
        else:
            self.forwardbutton.destroy()
            del self.forwardbutton


    def notify(self,event):
        if event.signal in ["going_to_planetary_mode_event","going_to_solar_system_mode_event","going_to_base_mode_event","going_to_company_window_event","going_to_firm_window_event","going_to_techtree_mode_event"]:
            self.history.append(self.current_event) 
            self.current_event = event
            if not self.protect_has_been_history:
                self.has_been_history = []
                try: self.forwardbutton
                except: pass
                else:
                    self.forwardbutton.sensitive = False
            while len(self.history) > global_variables.max_stepback_history_size:
                del self.history[0]
            try: self.backbutton
            except: pass
            else:
                self.backbutton.sensitive = True
        if event.signal == "update_infobox":
            try: self.window
            except:
                pass
            else:
                self.window.lock()
                self.data = self.update_data()
                info_label = Label(self.data)
                info_label.multiline = True
                self.window.set_children([info_label])
                self.window.update()
                self.window.unlock()
#        if event.signal == "infobox_toggle":
#            if not event.data:
#                try: self.window
#                except:
#                    self.create_infobox(self.renderer)
#                    #self.window.set_focus(True)
#                else:
#                    print "DEBUGGING: infobox was switched on, but already exists"
#            else:
#                self.exit()


    
    def update_data(self):
        date_string = str(self.solar_system_object_link.current_date)
        if self.solar_system_object_link.display_mode == "solar_system":
            env_string = "Solar system -" + string.capitalize(self.solar_system_object_link.current_planet.planet_name)
        elif self.solar_system_object_link.display_mode == "planetary":
            if self.solar_system_object_link.current_planet.current_base == None:
                env_string = self.solar_system_object_link.current_planet.planet_name
            else:
                env_string = self.solar_system_object_link.current_planet.planet_name + " - " + self.solar_system_object_link.current_planet.current_base.name 
        elif self.solar_system_object_link.display_mode == "planetary":
            env_string = self.solar_system_object_link.current_planet.current_base.name
        elif self.solar_system_object_link.display_mode == "company":
            env_string = self.solar_system_object_link.company_selected.name
        elif self.solar_system_object_link.display_mode == "firm":
            env_string = self.solar_system_object_link.firm_selected.name
        elif self.solar_system_object_link.display_mode == "base":
            env_string = self.solar_system_object_link.current_planet.current_base.name
        elif self.solar_system_object_link.display_mode == "techtree":
            env_string = "technology tree"
        else:
            env_string = ""
            if self.solar_system_object_link.message_printing["debugging"]:
                print_dict = {"text":"DEBUGGING: unknown display mode passed to infobox","type":"debugging"}
                self.solar_system_object_link.messages.append(print_dict)


            
            
        info_string = date_string + "\n" + env_string
        
        return info_string
    

        
        

        






class message_bar():
    """
    Class that receives messages for the player and prints them.
    It will show the message depending on the type. Types are:
    general gameplay info
    company_generation
    and more
    
    The message bar is visible at all times in the bottom of the screen.
    """
    def __init__(self,solar_system_object,action_surface,message_surface):
        self.solar_system_object_link = solar_system_object
        self.action_surface = action_surface
        self.message_surface = message_surface

        self.messages = []
        self.max_print_length = 6 #how many lines of text to print in standard viewing of the window
        self.max_save_length = 500 #how many lines of text to save in memory
        self.max_string_length = 140#how many letters is maximally allowed to be printed in the message window
        
        self.create()
        
        


    def create(self):
        """
        Function that will update the text field
        """
        self.message_surface.fill((212,212,212))
        pygame.draw.line(self.message_surface, (255,255,255), (0, 0), (self.message_surface.get_size()[0],0),2)        
        pygame.draw.line(self.message_surface, (255,255,255), (0, 0), (0,self.message_surface.get_size()[1]),2)

        
        #first trim the message list down to the number indicated to be max
        if len(self.messages) > self.max_save_length:
            surplus = len(self.messages) - self.max_save_length
            del self.messages[0:surplus]


        messages = []
        
        range_here = range(0,len(self.solar_system_object_link.messages))
        range_here.reverse()

        for i in range_here:
            message = self.solar_system_object_link.messages[i]
            if self.solar_system_object_link.message_printing[message["type"]]:
                messages.append(message)
            if len(messages) >= self.max_print_length:
                break
        messages.reverse()
        

        i = 0
        for message in messages:
            if self.solar_system_object_link.message_printing[message["type"]]:
                if len(message["text"]) > self.max_string_length:
                    message_text = message["text"][0:self.max_string_length]
                else:
                    message_text = message["text"]
                rendered_message_string = global_variables.standard_font_small.render(message_text,True,(0,0,0))
                self.message_surface.blit(rendered_message_string, (10,10 + i * 15))
                i = i + 1

        

        
      





class navigation_window():
    """
    The navigation window. Is controlled by a togglebutton in the commandbox. When visible it can be used for zooming and rotating.
    """
    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(500,50,190,170)
        self.action_surface = action_surface
        
        
        
    def zoom_in(self,label,function_parameter):
        return "zoom_in"
    
    def zoom_out(self,label,function_parameter):
        return "zoom_out"

    def rotate_west(self,label,function_parameter):
        return "go_west"

    def rotate_east(self,label,function_parameter):
        return "go_east"

    def rotate_south(self,label,function_parameter):
        return "go_south"

    def rotate_north(self,label,function_parameter):
        return "go_north"
    
    
    def receive_click(self,event):
        if pygame.Rect(self.rect[0] + 70, self.rect[1] + 10, 50, 30).collidepoint(event.pos) == 1:
            return self.button_north.activate(event.pos)
        if pygame.Rect(self.rect[0] + 20, self.rect[1] + 40, 50, 30).collidepoint(event.pos) == 1:
            return self.button_west.activate(event.pos)
        if pygame.Rect(self.rect[0] + 70, self.rect[1] + 70, 50, 30).collidepoint(event.pos) == 1:
            return self.button_south.activate(event.pos)
        if pygame.Rect(self.rect[0] + 120, self.rect[1] + 40, 50, 30).collidepoint(event.pos) == 1:
            return self.button_east.activate(event.pos)


        if pygame.Rect(self.rect[0] + 10, self.rect[1] + 120, 80, 30).collidepoint(event.pos) == 1:
            return self.button_zoom_in.activate(event.pos)
        if pygame.Rect(self.rect[0] + 100, self.rect[1] + 120, 80, 30).collidepoint(event.pos) == 1:
            return self.button_zoom_out.activate(event.pos)

    
    
    def create(self):
        """
        The creation function.  
        """

        pygame.draw.rect(self.action_surface, (212,212,212), self.rect)
        pygame.draw.rect(self.action_surface, (0,0,0), self.rect, 2)
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0] + self.rect[2], self.rect[1]))
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0], self.rect[1] + self.rect[3]))
        
        self.button_north = gui_components.button("N", self.action_surface, self.rotate_north, topleft = (self.rect[0] + 70, self.rect[1] + 10),fixed_size = (50,30))
        self.button_west = gui_components.button("W", self.action_surface, self.rotate_west, topleft = (self.rect[0] + 20, self.rect[1] + 40),fixed_size = (50,30))
        self.button_south = gui_components.button("S", self.action_surface, self.rotate_south, topleft = (self.rect[0] + 70, self.rect[1] + 70),fixed_size = (50,30))
        self.button_east = gui_components.button("E", self.action_surface, self.rotate_east, topleft = (self.rect[0] + 120, self.rect[1] + 40),fixed_size = (50,30))

        self.button_zoom_in = gui_components.button("Zoom in", self.action_surface, self.zoom_in, topleft = (self.rect[0] + 10, self.rect[1] + 120),fixed_size = (80,30))
        self.button_zoom_out = gui_components.button("Zoom out", self.action_surface, self.zoom_out, topleft = (self.rect[0] + 100, self.rect[1] + 120),fixed_size = (80,30))        



class overlay_window():
    """
    The overlay control window. Can be toggled from commandbox. When visible it can be used to control which visual overlays
    that can be seen in planet mode (topographical maps, resource maps etc)
    """
    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(500,50,200,250)
        self.action_surface = action_surface
        
    def overlay_set(self,type_of_overlay, function_parameter):
        sol = self.solar_system_object_link
        sol.current_planet.planet_display_mode = type_of_overlay
        surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()

#    def (self,button_name,function_parameter):
#        print "emitted display overlay with " + str(button_name)


    def receive_click(self,event):
        self.radiobuttons.activate(event.pos)


        
    def create(self):
        """
        The creation function. Doesn't return anything. 
        """
        
        pygame.draw.rect(self.action_surface, (212,212,212), self.rect)
        pygame.draw.rect(self.action_surface, (0,0,0), self.rect, 2)
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0] + self.rect[2], self.rect[1]))
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0], self.rect[1] + self.rect[3]))
        
        labels = ["visible light","trade network","topographical"] + self.solar_system_object_link.mineral_resources

        self.radiobuttons = gui_components.radiobuttons(labels, self.action_surface, self.overlay_set, function_parameter = None, topleft = (self.rect[0] + 10 , self.rect[1] + 10), selected = None)
        
        



class planet_jump_window():
    """
    The planet jump window. Can be toggled from commandbox. When visible it can be used as shortcut to planet view
    for the different planets
    """
    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(500,50,100,250)
        self.action_surface = action_surface
        
        
        
    def planet_jump(self,planet_name,function_parameter):
        print planet_name
        planet = self.solar_system_object_link.planets[planet_name] 
        self.solar_system_object_link.current_planet = planet
        print planet
        planet.load_for_drawing()
        self.solar_system_object_link.display_mode = "planetary"
        surface = planet.draw_entire_planet(planet.eastern_inclination,planet.northern_inclination,planet.projection_scaling)
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()
            
    

    
    def receive_click(self,event):
        offset = event.pos[1] - self.rect[1]
        index = (offset - 5) // 30
        if 0 <= index < len(self.button_labels):
            selection = self.buttons[self.button_labels[index]].activate(event.pos)
            if selection in self.solar_system_object_link.planets.keys():
                return self.solar_system_object_link.planets[selection]
            else:
                if self.solar_system_object_link.message_printing["debugging"]:
                    print_dict = {"text":"DEBUGGING: The planet jump function asked to go to a non-recognised planet","type":"debugging"}
                    self.solar_system_object_link.messages.append(print_dict)


    def create(self):
        """
        The creation function.  
        """
        pygame.draw.rect(self.action_surface, (212,212,212), self.rect)
        pygame.draw.rect(self.action_surface, (0,0,0), self.rect, 2)
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0] + self.rect[2], self.rect[1]))
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0], self.rect[1] + self.rect[3]))
        
        self.button_labels = ["mercury","venus","earth","mars","jupiter","saturn","uranus","neptune"]

        self.buttons = {}
        for i, button_label in enumerate(self.button_labels):
            self.buttons[button_label] = gui_components.button(button_label, self.action_surface, self.planet_jump, topleft = (self.rect[0] + 5, self.rect[1] + 5 + i * 30),fixed_size = (self.rect[2] - 10, 25))
            








class tech_window():
    """
    Class for the tech tree. Most of the actual algorithms are in techtree.py - this is just a shell for holding
    the notify system in the same structure as other GUI elements
    """
    def __init__(self,solar_system_object, action_surface):
        self.solar_system_object_link = solar_system_object
        self.action_surface = action_surface
        self.display_mode_before = "planetary"
        self.rect = pygame.Rect(0,0,0,0)
        

    def create(self):
        sol = self.solar_system_object_link
        sol.display_mode = "techtree"
        surface = sol.technology_tree.plot_total_tree(sol.technology_tree.vertex_dict,sol.technology_tree.zoomlevel,center = sol.technology_tree.center)
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()
        
    def receive_click(self,event):
        if self.solar_system_object_link.message_printing["debugging"]:
            print_dict = {"text":"DEBUGGING: tech window received a direct click. This should not be possible","type":"debugging"}
            self.solar_system_object_link.messages.append(print_dict)


class base_window():
    """
    This window shows an overview of all bases with options for fast jumping.
    """
    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface
        



    def create(self):
        """
        The creation function. ' 
        """
        
        base_data = {}
        for planet_instance in self.solar_system_object_link.planets.values():
            for base_instance in planet_instance.bases.values():
                
                if base_instance.for_sale:
                    for_sale = "For sale"
                else:
                    for_sale = ""
                
                data_here = {"Location":planet_instance.name,"Population":base_instance.population,"For sale":for_sale}

                base_data[base_instance.name] = data_here
                
        column_order = ["rownames","Location","Population","For sale"]
        
        self.fast_list = gui_components.fast_list(self.action_surface, base_data, self.rect, column_order)

    def receive_click(self,event):
        self.fast_list.receive_click(event)
        if event.button == 3:
            base_selected = None
            for planet_instance in self.solar_system_object_link.planets.values():
                for base_instance in planet_instance.bases.values():
                    if base_instance.name == self.fast_list.selected_name:
                        base_selected = base_instance
                        
            if base_selected is None:
                raise Exception("The base sought after (" + str(self.fast_list.selected_name) + ") was not found in the base list of the solar_system_object_link")
    
            self.solar_system_object_link.current_planet.current_base = base_selected
            self.solar_system_object_link.display_mode = "base"
            return "clear"

            
            


    def notify(self,event):
        if event.signal == "base_toggle":
            if not event.data:
                self.create_base_window()
            else:
                self.exit()
    
    def exit(self):
        try: self.window
        except: pass
        else:
            self.window.exit()
            del self.window
        try: self.link_button
        except: pass
        else:
            self.link_button.destroy()
            del self.link_button



class trade_window():
    """
    This windows shows an overview of all assets (bases and firms) and tech that is for sale, ie. all non-location specific offers.
    """
    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface
        

    def create(self):
        """
        The creation function. Doesn't return anything.
        """

        
        asset_and_tech_data = {}
        for planet_instance in self.solar_system_object_link.planets.values():
            for base_instance in planet_instance.bases.values():
                if base_instance.for_sale:
                    
                    data_here = {"Type":"base","Best price":"for auction (pop: " + str(base_instance.population) + ")","For sale by":base_instance.owner.name,"for_sale_by_link":[base_instance.owner],"object":base_instance}

                    asset_and_tech_data[base_instance.name] = data_here
                
        for company_instance in self.solar_system_object_link.companies.values():
            pass #FIXME add firms for sale here, whenever that is implemented
        
        for technology in self.solar_system_object_link.technology_tree.vertex_dict.values():
            if len(technology["for_sale_by"]) > 0:
                prices = technology["for_sale_by"].values()
                prices.sort()
                best_price = prices[-1]
                
                if len(technology["for_sale_by"]) == 1:
                    for_sale_by = str(technology["for_sale_by"].keys()[0].name)
                else:
                    for_sale_by = str(len(technology["for_sale_by"])) + " companies"
                for_sale_by_link = technology["for_sale_by"].keys()
                
                data_here = {"Type":"technology","Best price":best_price,"For sale by":for_sale_by,"for_sale_by_link":for_sale_by_link,"object":technology}
                asset_and_tech_data[technology["technology_name"]] = data_here
        
        column_order = ["rownames","Type","Best price","For sale by"]
        self.fast_list = gui_components.fast_list(self.action_surface, asset_and_tech_data, rect = self.rect, column_order = column_order)

    def receive_click(self,event):
        self.fast_list.receive_click(event)
        if event.button == 3:
            if self.fast_list.selected_name is not None:
                bid_on = self.fast_list.selected_name
                for_sale_by = self.fast_list.original_tabular_data[bid_on]["for_sale_by_link"]
                sale_object = self.fast_list.original_tabular_data[bid_on]["object"]
                type = self.fast_list.original_tabular_data[bid_on]["Type"]
                price = self.fast_list.original_tabular_data[bid_on]["Best price"]
                
                if type == "technology":
                    current_player = self.solar_system_object_link.current_player.known_technologies
                    check_result = self.solar_system_object_link.technology_tree.check_technology_bid(current_player,sale_object)
                    
                    if check_result != "ok":
                        print_dict = {"text":"Can not bid for " + sale_object["technology_name"] + " because it is " + check_result,"type":"general gameplay info"}
                        self.solar_system_object_link.messages.append(print_dict)
                        return None
                
                if len(for_sale_by) > 1:
                    if type != "technology":
                        raise Exception("A bid was made for a type: " + str(type) + " asset, with more than one seller. This should not be possible") 
                    sellers_data = {}
                    for seller in sale_object["for_sale_by"]:
                        price = sale_object["for_sale_by"][seller]
                        sellers_data[seller.name] = {"Price":price,"seller_link":seller}
                    
                    column_order = ["rownames","Price"]
                    
                    self.fast_list = gui_components.fast_list(self.surface,sellers_data,self.rect,column_order)
            
    #                self.perform_bid(sale_object, None, type, None)
            

    def chose_seller(self):
        """
        Function that allows players to choose between more than one seller
        """
        if self.fast_list.selected_name is not None:
            bid_on = self.fast_list.selected_name
            for_sale_by = self.fast_list.original_tabular_data[bid_on]["for_sale_by_link"]
            sale_object = self.fast_list.original_tabular_data[bid_on]["object"]
            type = self.fast_list.original_tabular_data[bid_on]["Type"]
            price = self.fast_list.original_tabular_data[bid_on]["Best price"]
            
            if type == "technology":
                current_player = self.solar_system_object_link.current_player.known_technologies
                check_result = self.solar_system_object_link.technology_tree.check_technology_bid(current_player,sale_object)
                
                if check_result != "ok":
                    print_dict = {"text":"Can not bid for " + sale_object["technology_name"] + " because it is " + check_result,"type":"general gameplay info"}
                    self.solar_system_object_link.messages.append(print_dict)
                    return None
            
            self.exit()
            if len(for_sale_by) > 1:
                if type != "technology":
                    raise Exception("A bid was made for a type: " + str(type) + " asset, with more than one seller. This should not be possible") 
                sellers_data = {}
                for seller in sale_object["for_sale_by"]:
                    price = sale_object["for_sale_by"][seller]
                    sellers_data[seller.name] = {"Price":price,"seller_link":seller}
                
                column_order = ["rownames","Price"]
                
                self.window = gui_components.fast_list(self.renderer)
                self.window.receive_data(sellers_data,column_order = column_order)
                self.window.topleft = self.topleft
                self.window.list_size = (self.list_size[0], self.list_size[1] / 2)
                self.window.create_fast_list()
                self.window.render_title()
        
                self.link_button = Button("Bid")
                self.link_button.topleft = (self.topleft[0] + self.list_size[0]/2 - self.link_button.size[0]/2,  self.topleft[1] + self.list_size[1]+50)
                self.link_button.connect_signal(Constants.SIG_CLICKED,self.perform_bid, sale_object, None, type, None)
                self.renderer.add_widget(self.link_button)
#                self.perform_bid(sale_object, None, type, None)
                
            else:
                
                self.perform_bid(sale_object, for_sale_by[0],type, price)

                
                        
    def perform_bid(self, sale_object, seller, type, price):
        """
        Function that allows the player to bid on an asset or technology
        """
        if seller is None: #then it is because we don't know what was chosen in chose_seller and we'll extract that
            bid_on = self.window.selected_name
            seller = self.window.original_tabular_data[bid_on]["seller_link"]
        if price is None: #then it is because we don't know what was chosen in chose_seller and we'll extract that
            bid_on = self.window.selected_name
            price = self.window.original_tabular_data[bid_on]["Price"]    
        
        self.exit(reset_commandbox_button = True)
        

        current_player = self.solar_system_object_link.current_player
        if current_player.capital > price:
            if type == "technology":
                
                
                    self.solar_system_object_link.current_player.known_technologies[sale_object["technology_name"]] = sale_object
                    current_player.capital = current_player.capital - price
                    seller.capital = seller.capital + price
                    print_dict = {"text":str(sale_object["technology_name"]) + " was bought for " + str(price) + " from " + str(seller.name),"type":"general gameplay info"}
                    self.solar_system_object_link.messages.append(print_dict)
                     
                    
            elif type == "base":
                    print_dict = {"text":"base buying not implemented yet","type":"general gameplay info"}
                    self.solar_system_object_link.messages.append(print_dict)
    
            else:
                raise Exception("Unknown type: " + str(type) + " asked for in the asset sales GUI")
    
                
        else:
            print_dict = {"text":current_player.name + " has a capital of " + str(current_player.capital) + " and can't bid " + str(price),"type":"general gameplay info"}
            self.solar_system_object_link.messages.append(print_dict)
            
                
    
    

    def notify(self,event):
        if event.signal == "trade_toggle":
            if not event.data:
                self.create_trade_window()
            else:
                self.exit()
    


class company_window():
    """
    The company overview window. Can be toggled from commandbox. Shows all companies in the solarsystem, along with some info
    about them. Can be used as shortcut to the company of interest.
    """
    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface
        
 
    def create(self):
        """
        The creation function. 
        """
        
        company_data = {}
        for company_name in self.solar_system_object_link.companies:
            company_instance = self.solar_system_object_link.companies[company_name]
            capital = company_instance.capital
            no_of_firms = len(company_instance.owned_firms)
            no_of_cities = len(company_instance.home_cities)
            data_here = {"capital":capital,"owned firms":no_of_firms,"home cities":no_of_cities}
            if len(company_name)> global_variables.max_letters_in_company_names:
                if self.solar_system_object_link.message_printing["debugging"]:
                    print_dict = {"text":"DEBUGGING: Shortened " + str(company_name) + " to " + str(company_name[0:30]),"type":"debugging"}
                    self.solar_system_object_link.messages.append(print_dict)
                company_name = company_name[0:global_variables.max_letters_in_company_names]
            company_data[company_name] = data_here
        
        column_order = ["rownames","capital","owned firms","home cities"]
        
        self.fast_list = gui_components.fast_list(self.action_surface, company_data, rect = self.rect, column_order = column_order)

                

    def receive_click(self,event):
        self.fast_list.receive_click(event)
        if event.button == 3:

            if self.fast_list.selected_name in self.solar_system_object_link.companies.keys():
                selected_company = self.solar_system_object_link.companies[self.fast_list.selected_name]
                self.solar_system_object_link.display_mode = "company"
                self.solar_system_object_link.company_selected = selected_company
                return "clear"

            else:
                print_dict = {"text":"DEBUGGING:  " + str(self.fast_list.selected_name) + " was not found in company database","type":"debugging"}
                self.solar_system_object_link.messages.append(print_dict)
                











class file_window():
    """
    The file window. Can be toggled from commandbox. Quitting, saving, loading, settings and all the usual stuff you'd
    expect to find such a place.
    """
    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,400,500)
        self.action_surface = action_surface
        self.text_receiver = None 
        self.distribute_click_to_subwindow = None
        
        
        self.button_structure = {
                           "File menu":{
                                   "Save game":self.select_save_name,
                                   "Load game":self.select_game_to_load,
                                   "New game":self.new_game,
                                   "Game settings":"Game settings",
                                   "Automation settings":self.automation_settings,
                                   "Message settings":self.message_settings,
                                   "Quit game":"Quit game"},
                           "Quit game":{
                                        "Ok":self.quit,
                                        "Cancel":"File menu",
                                        "Save first":self.select_save_name
                                    },
                           "Game settings":{
                                        "Game speed":self.game_speed_settings,
                                        "Difficulty":"File menu",
                                        "Catastrophes":"Catastrophe window"
                                            },
                           "Catastrophe window":{
                                                 "Global warming":self.raise_waters,
                                                 "Global cooling":self.lower_waters,
                                                 "Meteor strike":"Catastrophe window",
                                                 "Nuclear war":self.nuclear_war,
                                                 "Lunar explosion":self.nuclear_war,
                                                 "Skynet uprising":"Catastrophe window"
                                                 }
                           
                           }




    def create(self):
        """
        The creation function.  
        """
        self.button_instances_now = {}
        self.button_list_now = []
        self.distribute_click_to_subwindow = None
        self.position = "File menu"
        self.draw()

    def draw(self):
        self.button_instances_now = {}
        pygame.draw.rect(self.action_surface, (150,150,150), self.rect)
        
        self.button_list_now = self.button_structure[self.position].keys()
        self.button_list_now.sort()
        
        for i, button_name in enumerate(self.button_list_now):
            if isinstance(self.button_structure[self.position][button_name], str): # has a submenu
                self.button_instances_now[button_name] = gui_components.button(button_name,
                                                    self.action_surface,
                                                    self.go_to_submenu,
                                                    function_parameter = self.button_structure[self.position][button_name],
                                                    fixed_size = (self.rect[2] - 20, 35),
                                                    topleft = (10 + self.rect[0], i * 40 + 10 + self.rect[1])
                                                    )
            else: # has a subfunction
                self.button_instances_now[button_name] = gui_components.button(button_name,
                                                    self.action_surface,
                                                    self.button_structure[self.position][button_name],
                                                    function_parameter = None,
                                                    fixed_size = (self.rect[2] - 20, 35),
                                                    topleft = (10 + self.rect[0], i * 40 + 10 + self.rect[1])
                                                    )
            
            
        pygame.display.flip()


    def go_to_submenu(self, label, function_parameter):
        """
        Function that accepts activations from buttons that leads to submenus
        """
        self.position = function_parameter
        self.draw()

    
    def receive_click(self,event):
        if self.distribute_click_to_subwindow is None:
            if isinstance(event.pos[1],int):
                index = (event.pos[1] - self.rect[1] - 10) / 40
                if index >= 0 and index < len(self.button_list_now):
                    button_pressed = self.button_list_now[index]
                    if button_pressed != "Empty space":
                        self.button_instances_now[button_pressed].activate(event.pos)
        else:
            self.distribute_click_to_subwindow.receive_click(event)



    def quit(self,label,function_parameter):
        sys.exit(0)


    
            

    def select_save_name(self,label, function_parameter):
        """
        Prompts the player to input the name of the savegame file
        """
        
        pygame.draw.rect(self.action_surface, (150,150,150), self.rect)
        description = global_variables.standard_font.render("Enter savegame name:",True,(0,0,0))
        self.action_surface.blit(description, (10 + self.rect[0], 10 + self.rect[1]))
        
        self.button_list_now = ["Empty space","Name box","Ok"]
        self.button_instances_now = {}
        self.button_instances_now["Name box"] = gui_components.entry(self.action_surface, 
                             topleft = (10 + self.rect[0], 10 + 40 + self.rect[1]), 
                             width = self.rect[2] - 20, 
                             max_letters = global_variables.max_letters_in_company_names)

        self.text_receiver = self.button_instances_now["Name box"]
        self.button_instances_now["Name box"].active = True 
        
        self.button_instances_now["Ok"] = gui_components.button(
                                    "Ok",
                                    self.action_surface,
                                    self.effectuate_save,
                                    function_parameter = None,
                                    fixed_size = (self.rect[2] - 20, 35),
                                    topleft = (10 + self.rect[0], 80 + 10 + self.rect[1])
                                    )
        pygame.display.flip() 
        
        
    def effectuate_save(self,label,function_parameter):
        save_game_name = self.button_instances_now["Name box"].text
        self.solar_system_object_link.save_solar_system(os.path.join("savegames",save_game_name))
        self.create()
        

    def select_game_to_load(self, label, function_parameter):
        load_window = gui_components.fast_list(self.action_surface, os.listdir("savegames"), rect = self.rect)
        self.distribute_click_to_subwindow = load_window                                            

    def effectuate_load(self):
        load_file_name = self.distribute_click_to_subwindow.text
        if load_file_name is not None:
            self.solar_system_object_link.load_solar_system(os.path.join("savegames",load_file_name))
    
        

    def new_game(self, label, function_parameter):
        print "should start new game"







    def automation_settings(self,label,function_parameter):
        """
        The window that is shown when asking for automation_settings.
        First destroys the previous file window
        """
        
        
        
        if self.solar_system_object_link.current_player is None:
            if self.solar_system_object_link.message_printing["debugging"]:
                print_dict = {"text":"DEBUGGING: Game is in simulation mode so no changes can be made","type":"debugging"}
                self.solar_system_object_link.messages.append(print_dict)
        else:
            pygame.draw.rect(self.action_surface, (150,150,150), self.rect)
            
            self.button_instances_now = {}
            self.button_list_now = []

            button_names = self.solar_system_object_link.current_player.automation_dict.keys()

            for i, button_name in enumerate(button_names):
                self.button_list_now.append(button_name)
                
                self.button_instances_now[button_name] = gui_components.togglebutton(button_name,
                                                          self.action_surface,
                                                          self.change_automation,
                                                          function_parameter = button_name,
                                                          fixed_size = (self.rect[2] - 20, 35),
                                                          topleft = (10 + self.rect[0], i * 40 + 10 + self.rect[1]),
                                                          pressed = self.solar_system_object_link.current_player.automation_dict[button_name]
                                                    )
            
            
            self.button_list_now.append("Decision variables")
            self.button_instances_now["Decision variables"] = gui_components.button(
                                                                           "Decision variables",
                   self.action_surface,
                   self.decision_variables,
                   function_parameter = None,
                   fixed_size = (self.rect[2] - 20, 35),
                   topleft = (10 + self.rect[0], (i + 1) * 40 + 10 + self.rect[1]),
                   )
            
            
            

    def change_automation(self,label,function_parameter):
        """
        Function that will effectuate the change of automation status
        """
        if self.solar_system_object_link.current_player is None:
            raise Exception("No player selected")
        if function_parameter not in self.solar_system_object_link.current_player.automation_dict.keys():
            raise Exception("The automation_type " + str(function_parameter) + " was not found in the automation_dict")
        previous_setting = self.solar_system_object_link.current_player.automation_dict[function_parameter]
        self.solar_system_object_link.current_player.automation_dict[function_parameter] = not previous_setting

        print_dict = {"text":"For " + self.solar_system_object_link.current_player.name + " the " + str(function_parameter) + " was changed from " + str(previous_setting) + " to " + str(not previous_setting),"type":"general company info"}
        self.solar_system_object_link.messages.append(print_dict)
#        self.manager.emit("update_infobox", None)
        
        

    def decision_variables(self,label,function_parameter):
        """
        The window that is shown when asking for decision_variables.
        """

        if self.solar_system_object_link.current_player is None:
            if self.solar_system_object_link.message_printing["debugging"]:
                print_dict = {"text":"DEBUGGING: Game is in simulation mode so no changes can be made","type":"debugging"}
                self.solar_system_object_link.messages.append(print_dict)
        else:
            pygame.draw.rect(self.action_surface, (150,150,150), self.rect)
            decision_variables_window = gui_components.fast_list(self.action_surface, 
                                                                 self.solar_system_object_link.current_player.company_database.keys(),
                                                                 rect = self.rect)

            self.distribute_click_to_subwindow = decision_variables_window                                            

            
        


    def check_and_save_decision_variables(self):
        """
        Function that checks that all variables in the entry boxes of the automation settings are integers between 1-100,
        and saves them if this is correct
        """
        
#        table = self.window
        all_passed_check = True
        for column_offset in [0,2]:
            for row_index in range(0,self.window.rows - 1): #don't count the last row with buttons
                if self.window.grid[(row_index, column_offset)] is not None:
                    name = self.window.grid[(row_index, column_offset)].text
                    value = self.window.grid[(row_index, column_offset + 1)].text
                    try:    int(value)
                    except: 
                        print_dict = {"text":"The value " + str(value) + " at " + str(name) + " is not integer","type":"general gameplay info"}
                        self.solar_system_object_link.messages.append(print_dict)
                        self.manager.emit("update_infobox", None)
                        all_passed_check = False
                        break
                    else:   
                        pass
                    
                    value_as_int = int(value)
                    
                    if 1 <= value_as_int <= 100:
                        pass
                    else:
                        print_dict = {"text":"The value " + str(value) + " at " + str(name) + " is not between 1 and 100","type":"general gameplay info"}
                        self.solar_system_object_link.messages.append(print_dict)
                        self.manager.emit("update_infobox", None)
                        all_passed_check = False
                        break
 
        if all_passed_check:
            print_dict = {"text":"The decision matrix has been updated for " + self.solar_system_object_link.current_player.name,"type":"general gameplay info"}
            self.solar_system_object_link.messages.append(print_dict)
            self.manager.emit("update_infobox", None)
            for column_offset in [0,2]:
                for row_index in range(0,self.window.rows - 1): #don't include rows with buttons
                    if self.window.grid[(row_index, column_offset)] is not None:
                        name = self.window.grid[(row_index, column_offset)].text
                        value = self.window.grid[(row_index, column_offset + 1)].text
                        value_as_int = int(value)
                        
                        self.solar_system_object_link.current_player.company_database[name] = value_as_int
            
            self.exit(True)
            


    def message_settings(self, label, function_parameter):
        """
        Function that decides what messages should be shown
        """
        pygame.draw.rect(self.action_surface, (150,150,150), self.rect)

        button_names = self.solar_system_object_link.message_printing.keys()

        self.button_instances_now = {}
        self.button_list_now = []

        for i, button_name in enumerate(button_names):
            self.button_list_now.append(button_name)
            
            self.button_instances_now[button_name] = gui_components.togglebutton(button_name,
                                                      self.action_surface,
                                                      self.change_message_setting,
                                                      function_parameter = button_name,
                                                      fixed_size = (self.rect[2] - 20, 35),
                                                      topleft = (10 + self.rect[0], i * 40 + 10 + self.rect[1]),
                                                      pressed = self.solar_system_object_link.message_printing[button_name]
                                                )


    def change_message_setting(self, label, function_parameter):                        
        """
        Function that will effectuate the change of message settings
        """
        if function_parameter not in self.solar_system_object_link.message_printing.keys():
            raise Exception("The message type " + str(function_parameter) + " was not found in the message_printing dict")
        previous_setting = self.solar_system_object_link.message_printing[function_parameter]
        self.solar_system_object_link.message_printing[function_parameter] = not previous_setting

        print_dict = {"text":"The show-settings for " + str(function_parameter) + " was changed from " + str(previous_setting) + " to " + str(not previous_setting),"type":"general gameplay info"}
        self.solar_system_object_link.messages.append(print_dict)
#        self.manager.emit("update_infobox", None)
                        
    
        

    

        
    def game_speed_settings(self, label, function_parameter):
        """
        The window that is shown when asking for time delay settings
        Time delay settings is defined as a value between 0 and 100 with 100 being the fastest.
        It translates into the self.solar_system_object_link.step_delay_time
        which is a value between 0 (perform game-iteration at every loop-iteration) and infinity (but then the game will stop)
        a loop-iteration is the time it takes to react to clicks etc + 15 milliseconds (but check value pygame.time.delay in main 
        document to be sure). A game-iteration is all the movement of planets, thinking of companies etc.
        
        We here define the range of self.solar_system_object_link.step_delay_time as given in step_delay_time_range. This is certainly up to testing.
        In any case it means that the lowest value of step_delay_time_range equals time delays settings of 100 (max speed) and the highest
        value of step_delay_time_range equals time delay settings of 0 (slowest speed)
        """
        pygame.draw.rect(self.action_surface, (150,150,150), self.rect)

        delay_range = (10,500)

        old_game_speed = self.solar_system_object_link.step_delay_time

        button_names = self.solar_system_object_link.message_printing.keys()
        
        
        fastest = global_variables.standard_font.render("Fastest",True,(0,0,0))
        self.action_surface.blit(fastest, (self.rect[0] + 50, self.rect[1] + 40))

        slowest = global_variables.standard_font.render("Slowest",True,(0,0,0))
        self.action_surface.blit(slowest, (self.rect[0] + 50, self.rect[1] + self.rect[3]-  50))
        
        
        def execute(label, function_parameter):
            game_speed = self.distribute_click_to_subwindow.position / 30
            self.solar_system_object_link.step_delay_time = self.distribute_click_to_subwindow.position
        
        self.distribute_click_to_subwindow = gui_components.vscrollbar (self.action_surface,
                                                execute,
                                                topleft = (self.rect[0] + 10, self.rect[1] + 30),
                                                length_of_bar_in_pixel = self.rect[3] - 60,
                                                range_of_values = delay_range,
                                                start_position = old_game_speed
                                                )

#    def catastrophe_window(self, label, function_parameter):
#        """
#        The window that is shown when asking for catastrophes
#        """
#        
#        button_names = ["Global warming","Global cooling","Meteor strike","Nuclear war","Lunar explosion","Skynet uprising"]
#        button_functions = [self.raise_waters,self.lower_waters,self.exit,self.nuclear_war,self.exit,self.exit]
#        
#        for i, button_name in enumerate(button_names):
#            temp_button = Button(button_name)
#            temp_button.connect_signal(SIG_CLICKED,button_functions[i])
#            max_width = max(max_width,temp_button.width)
#            list_of_children.append(temp_button)
#        
#        for button in list_of_children:
#            button.set_minimum_size(max_width,button.size[1])
#        
#        ok_button = Button("Ok")
#        ok_button.connect_signal(SIG_CLICKED,self.exit,True)
#        
#        self.window.set_children(list_of_children + [Label(""), ok_button])
#
#        self.renderer.add_widget(self.window)

    def raise_waters(self,label,function_parameter):
        """
        Function to raise waters
        """
        sol = self.solar_system_object_link

        if sol.display_mode == "planetary":
            sol.current_planet.change_water_level(sol.current_planet.water_level + 0.5)
            surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)
        else:
            return
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()


    def lower_waters(self,label,function_parameter):
        sol = self.solar_system_object_link

        if sol.display_mode == "planetary":
            sol.current_planet.change_water_level(sol.current_planet.water_level - 0.5)                        
            surface = sol.current_planet.draw_entire_planet(sol.current_planet.eastern_inclination,sol.current_planet.northern_inclination,sol.current_planet.projection_scaling)
        else:
            return
        self.action_surface.blit(surface,(0,0))
        pygame.display.flip()


    def nuclear_war(self,label,function_parameter):
        sol = self.solar_system_object_link
        if sol.display_mode == "planetary":
            earth = sol.planets["earth"]
            base_names_chosen = ["stockholm","glasgow","bremen","rotterdam","stuttgart","genoa"]
            bases_chosen = {}
            for base_name_chosen in base_names_chosen:
                bases_chosen[base_name_chosen] = earth.bases[base_name_chosen]
            earth.explode(56,10,bases_chosen,self.action_surface)
        else:
            return

        

    def quit_dialog(self):
        """
        The window that is shown when quittting.
        """
        def _result (result, dialog):
            if result == DLGRESULT_OK:
                sys.exit(0)
            elif result == DLGRESULT_CANCEL:
                dialog.destroy ()
            elif result == DLGRESULT_USER:
                dialog.destroy ()
        buttons = [Button ("#OK"), Button ("#Cancel"), Button ("#Save first")]
        results = [DLGRESULT_OK, DLGRESULT_CANCEL, DLGRESULT_USER]
        dialog = GenericDialog ("Generic dialog", buttons, results)
        lbl = Label ("Do you really want to quit?")
        dialog.content.add_child (lbl)
        dialog.connect_signal (SIG_DIALOGRESPONSE, _result, dialog)
        dialog.topleft = 30, 30
        dialog.depth = 1
        return dialog
    
















class base_population_info():
    """
    Subview of the base view. Shows miscellanous information about a base, such as stock, trade routes and population.
    """

    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface
        
    def receive_click(self,event):
        self.fast_list.receive_click(event)

    def create(self):
        """
        The creation function.  
        """
        base_selected = self.solar_system_object_link.current_planet.current_base
        if base_selected is not None:
            base_population_dict= {}
            base_population_dict["Owner"] = {"info":base_selected.owner.name}
            base_population_dict["GDP per capita"] = {"info":base_selected.gdp_per_capita_in_dollars}
            base_population_dict["Position: east"] = {"info":str(base_selected.position_coordinate[0])}
            base_population_dict["Position: north"] = {"info":str(base_selected.position_coordinate[1])}
            base_population_dict["Population"] = {"info":base_selected.population}
            base_population_dict["Bitternes"] = {"info":base_selected.bitternes_of_base}
            base_population_dict["Wages"] = {"info":base_selected.wages}
            
            for resource in base_selected.mining_opportunities:
                 base_population_dict["Mining: " + resource] = {"info":base_selected.mining_opportunities[resource]["sum_of_resources"]}
            
            for resource in base_selected.stock_dict:
                 base_population_dict["Stock: " + resource] = {"info":base_selected.stock_dict[resource]}

            for resource in base_selected.input_output_dict["input"]:
                 base_population_dict["Input: " + resource] = {"info":base_selected.input_output_dict["input"][resource]}

            
            base_population_dict["Trade routes, number of"] = {"info":str(len(base_selected.trade_routes))}
            if 0 < len(base_selected.trade_routes) < 4:
                list_value = str(base_selected.trade_routes.keys())
                list_value = list_value.rstrip("]")
                list_value = list_value.lstrip("[")
                base_population_dict["Trade routes"] = {"info":list_value}
            

            self.fast_list = gui_components.fast_list(self.action_surface, base_population_dict, rect = self.rect, column_order = ["rownames","info"])
        else:
            print "DEBUGGING: Base selected was None"





class base_list_of_companies():
    """
    Subview of the base view. Shows a list of all companies operating in the base. Shortcut button to zoom in on one of these companies.
    """

    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface
        

    def receive_click(self,event):
        self.fast_list.receive_click(event)
        if event.button == 3:
            
            if self.fast_list.selected_name in self.solar_system_object_link.companies.keys():
                selected_company = self.solar_system_object_link.companies[self.fast_list.selected_name]
                self.solar_system_object_link.display_mode = "company"
                self.solar_system_object_link.company_selected = selected_company
                return "clear"

            else:
                print_dict = {"text":"DEBUGGING:  " + str(self.fast_list.selected_name) + " was not found in company database","type":"debugging"}
                self.solar_system_object_link.messages.append(print_dict)
                


    def create(self):
        """
        The creation function.  
        """

        company_data = {}
        for company_instance in self.solar_system_object_link.companies.values():
            if self.solar_system_object_link.current_planet.current_base.name in company_instance.home_cities.keys():
                company_data[company_instance.name] = {}
                company_data[company_instance.name]["capital"] = company_instance.capital
                
                owned_firms_here = 0
                for firm_instance in company_instance.owned_firms.values():
                    if firm_instance.location == self.solar_system_object_link.current_planet.current_base:
                         owned_firms_here = owned_firms_here + 1
                         
                company_data[company_instance.name]["local firms"] = owned_firms_here
        
            
        self.fast_list = gui_components.fast_list(self.action_surface, company_data, rect = self.rect)
            


class base_list_of_firms():
    """
    Subview of the base view. Shows a list of all firms operating in the base. Shortcut button to zoom in on one of these firms.
    """

    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface
        

        
    

        

    def create(self):
        """
        The creation function.  
        """
        list_of_firms_in_base = []
        for company_instance in self.solar_system_object_link.companies.values():
            for firm_instance in company_instance.owned_firms.values():
                if not isinstance(firm_instance, company.merchant):
                    if firm_instance.location == self.solar_system_object_link.current_planet.current_base:
                        list_of_firms_in_base.append(firm_instance)
                else:
                    if firm_instance.from_location == self.solar_system_object_link.current_planet.current_base or firm_instance.to_location == self.solar_system_object_link.current_planet.current_base:
                        list_of_firms_in_base.append(firm_instance)
#        print list_of_firms_in_base
        firm_data = {}
        self.links = {}
        for firm_instance in list_of_firms_in_base:
            firm_data[firm_instance.name] = {}
            try: firm_instance.last_profit
            except: 
                firm_data[firm_instance.name]["last profit"] = "NA"
            else: 
                firm_data[firm_instance.name]["last profit"] = firm_instance.last_profit
            
            firm_data[firm_instance.name]["owner"] = firm_instance.owner.name
            self.links[firm_instance.name] = firm_instance
            
            stock_amount = 0
            for stock_item in firm_instance.stock_dict.values():
                stock_amount = stock_amount + stock_item
            firm_data[firm_instance.name]["stock size"] = stock_amount
        
        self.fast_list = gui_components.fast_list(self.action_surface, 
                                                  firm_data, 
                                                  rect = self.rect,
                                                  column_order = ["rownames","owner","stock size","last profit"]
                                                  )
        
    
    def receive_click(self,event):
        self.fast_list.receive_click(event)
        if event.button == 3:
            firm_selected = self.links[self.fast_list.selected_name]
            self.solar_system_object_link.display_mode = "firm"
            self.solar_system_object_link.firm_selected = firm_selected
            return "clear"




class base_and_firm_market_window():
    """
    Subview of the base view and also of the firm view. Shows information about the market in the base. For a chosen resource this can be either
    a history of what transactions has been made, or an overview of the bids currently in effect.
    
    This is also the interface where manual bids can be made
    """

    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface
        

        self.resource_selected = self.solar_system_object_link.trade_resources.keys()[0]
        self.graph_rect = pygame.Rect(200,100,400,400)


        self.frame_size = 40
        self.blank_area_in_middle_height = 30 #the middle area in the market bid mode
        self.graph_selected = "history"
        self.positional_database = {"bidding_mode":{},"non_bidding_mode":{}} #can be filled with information about clicks that the graphs receive
        self.highlighted_transactions = []
        self.bidding_mode = False #if click on the map should result in bidding


    def trade_resource_set_callback(self,label,function_parameter):
        self.resource_selected = label
        self.update_data(None, None)

    def graph_mode_callback(self,label,function_parameter):
        self.graph_selected = label
        self.update_data(None, None)    


    def market_selection_callback(self,label,function_parameter):
        self.base_selected_for_merchant = function_parameter[label]
        self.update_data(None, None)
#        
    def place_bid_callback(self,label,function_parameter):
        self.bidding_mode = label

    
    def create(self):
        """
        The creation function. Doesn't return anything, but saves and renders using the self.renderer. 
        """

        pygame.draw.rect(self.action_surface, (212,212,212), self.rect)
        pygame.draw.rect(self.action_surface, (0,0,0), self.rect, 2)
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0] + self.rect[2], self.rect[1]))
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0], self.rect[1] + self.rect[3]))
        
        #first making a list of the resources that should be displayed
        if self.solar_system_object_link.display_mode == "base":
            resource_button_names = self.solar_system_object_link.trade_resources.keys()
        elif self.solar_system_object_link.display_mode == "firm":
            firm_selected = self.solar_system_object_link.firm_selected
            if isinstance(firm_selected, company.merchant):
                resource_button_names = [firm_selected.resource, firm_selected.transport_type]
            else:
                resource_button_names = []
                for put in ["input","output"]:
                    for resource in firm_selected.input_output_dict[put]:
                        resource_button_names.append(resource)
        else:
            raise Exception("The display mode " + str(self.solar_system_object_link.display_mode) + " is not supposed to show market data")

        if self.resource_selected not in resource_button_names:
            self.resource_selected = resource_button_names[0]

        #for each resource to be displayed we make a radio button
        self.resource_buttons = gui_components.radiobuttons(
                                                        resource_button_names, 
                                                        self.action_surface, 
                                                        function = self.trade_resource_set_callback, 
                                                        function_parameter = None, 
                                                        topleft = (self.rect[0] + 10 , self.rect[1] + 10), 
                                                        selected = self.resource_selected)
        
        
        self.graph_buttons = gui_components.radiobuttons(
                                                        ["history","market bids"], 
                                                        self.action_surface, 
                                                        function = self.graph_mode_callback, 
                                                        function_parameter = None, 
                                                        topleft = (self.rect[0] + 10 , self.rect[1] + 40 + self.resource_buttons.rect[3]),
                                                        selected = self.graph_selected)

        
        
        #in case it is a merchant selected we have to also pick the markets looked upon.
        if self.solar_system_object_link.display_mode == "firm":
            firm_selected = self.solar_system_object_link.firm_selected
            if isinstance(firm_selected, company.merchant):
                self.market_selection_buttons = gui_components.radiobuttons(
                                                        ["From: " + firm_selected.from_location.name,"To: " + firm_selected.to_location.name], 
                                                        self.action_surface, 
                                                        function = self.market_selection_callback, 
                                                        function_parameter = {"From: " + firm_selected.from_location.name:firm_selected.from_location,"To: " + firm_selected.to_location.name:firm_selected.to_location}, 
                                                        topleft = (self.rect[0] + 10 , self.graph_buttons.rect[1] + self.graph_buttons.rect[3] + 40),
                                                        selected = "From: " + firm_selected.from_location.name)

                self.base_selected_for_merchant = firm_selected.from_location

                
            else:
                self.market_selection_buttons = None
                
        elif self.solar_system_object_link.display_mode == "base":
            self.market_selection_buttons = None
            firm_selected = self.solar_system_object_link.current_planet.current_base 
        else:
            raise Exception("Unknown display_mode: " + str(global_variabes.display_mode))
                    
        #Add an update button that allows for updates to be done
        try:    self.market_selection_buttons.rect
        except: update_button_topleft = (self.rect[0] + 10, self.graph_buttons.rect[1]+ self.graph_buttons.rect[3] + 20)
        else:   update_button_topleft = (self.rect[0] + 10, self.market_selection_buttons.rect[1]+ self.market_selection_buttons.rect[3] + 20)   

        
        self.update_button = gui_components.button("Update",
                                                   self.action_surface,
                                                   function = self.update_data,
                                                   function_parameter = None, 
                                                   topleft = update_button_topleft, 
                                                   fixed_size = None)
        


        
        #Finally, in case the firm selected is owned by the player, we add a "make market bid button"
        if firm_selected.name in self.solar_system_object_link.current_player.owned_firms.keys():
            self.bid_button = gui_components.togglebutton("Make market bid",
                                           self.action_surface,
                                           function = self.place_bid_callback,
                                           function_parameter = None, 
                                           topleft = (self.rect[0] + 10, self.update_button.rect[1] + self.update_button.rect[3] +20), 
                                           fixed_size = None)

            
            self.bidding_mode = False
        else:
            self.bid_button = None
            self.bidding_mode = False
            
        self.update_data(None, None)
            
        
    def update_data(self, label, function_parameter):
        """
        Function to update the data in the market analysis window. Its most important function is that it calls the relevant
        analysis function (market bids or market history) depending on the self.graph_selected variable.
        """
        
        self.highlighted_transactions = []
        if self.graph_selected == "market bids":
            surface = self.update_data_market_bids()
        elif self.graph_selected == "history":
            surface = self.update_data_history()
        else:
            raise Exception("Unknown graph type " + self.graph_selected)

        if not isinstance(surface,pygame.Surface):
            print self.graph_selected
            print surface
            print self.update_data_history()
            print self.update_data_market_bids()
            raise Exception("The surface returned in the market window was not recognised")
        
        self.action_surface.blit(surface, (self.graph_rect[0],self.graph_rect[1]))
        pygame.display.flip()


    def update_data_market_bids(self):
        """
        Function that draws a stock-market style surface with all the sell and buy bids that currently exists for a given resource
        """
        if self.solar_system_object_link.current_planet.current_base is None:
            raise Exception("A market bid window was requested at a time when the selected base was None")
        else:
            resource = self.resource_selected
            
            
            #first determining which market to look at. If in base mode it is obvious which. In firm for non-merchants it is home city, and for merchant it should be selectable
            if self.solar_system_object_link.display_mode == "base":
                market = self.solar_system_object_link.current_planet.current_base.market
            elif self.solar_system_object_link.display_mode == "firm":
                firm_selected = self.solar_system_object_link.firm_selected
                if isinstance(firm_selected, company.merchant):
                    market = self.base_selected_for_merchant.market
                else:
                    market = firm_selected.location.market
            else:
                raise Exception("The display mode " + str(self.solar_system_object_link.display_mode) + " is not supposed to show market data")

            #painting the basic market_analysis surface
            market_analysis_surface = pygame.Surface((self.graph_rect[2],self.graph_rect[3]))
            market_analysis_surface.fill((212,212,212))
            pygame.draw.line(market_analysis_surface,(50,50,50),(0,self.graph_rect[3]*0.5+7),(self.graph_rect[3],self.graph_rect[3]*0.5+7),3)
            pygame.draw.line(market_analysis_surface,(50,50,50),(0,self.graph_rect[3]*0.5-7),(self.graph_rect[3],self.graph_rect[3]*0.5-7),3)
            
            #making lists of quantitites, prices and providers
            quantities = []
            prices = []
            provider = []
            for offer_type in ["sell_offers","buy_offers"]:
                offers = market[offer_type][resource]
                for offer in offers:
                    quantities.append(offer["quantity"])
                    prices.append(offer["price"])
                    if "seller" in offer.keys():
                        provider.append(offer["seller"])
                    elif "buyer" in offer.keys():
                        provider.append(offer["buyer"])
                    else:
                        raise Exception("An offer was found in which there was neither seller nor buyer")
            
            
            if len(prices)==0:
                market_price_label = global_variables.standard_font.render("No " + resource + " on market",True,(0,0,0))
                market_analysis_surface.blit(market_price_label,(0,self.graph_rect[3]*0.5-5))
            else:
                #calculating max price and market price. Adding these as labels if relevant.
                max_price = max(prices)
                min_price = min(prices)
                max_quantity = max(quantities)
                sell = global_variables.standard_font.render("Max sell price: " + "%.5g" % max_price,True,(0,0,0))
                buy = global_variables.standard_font.render("Min buy price: " + "%.5g" % min_price,True,(0,0,0))
                if len(market["buy_offers"][resource]) == 0:
                    market_price = market["sell_offers"][resource][0]["price"]
                    market_price_description = "Only sell offers. Lowest is: " + "%.5g" % market["sell_offers"][resource][0]["price"]
                    market_analysis_surface.blit(sell,(0,0))
                elif len(market["sell_offers"][resource]) == 0:
                    market_price = market["buy_offers"][resource][0]["price"]
                    market_price_description = "Only buy offers. Highest is: " + "%.5g" % market["buy_offers"][resource][0]["price"]
                    market_analysis_surface.blit(buy,(0,self.graph_rect[3]-15))

                else:
                    market_price_description = "Highest buy offer: " + "%.5g" % market["buy_offers"][resource][0]["price"] + ". Lowest sell offer: " + "%.5g" % market["sell_offers"][resource][0]["price"] 
                    market_price = (market["sell_offers"][resource][0]["price"] + market["buy_offers"][resource][0]["price"]) * 0.5
                    market_analysis_surface.blit(sell,(0,0))
                    market_analysis_surface.blit(buy,(0,self.graph_rect[3]-15))
                market_price_label = global_variables.standard_font.render(market_price_description,True,(0,0,0))
                market_analysis_surface.blit(market_price_label,(self.graph_rect[2]/100,self.graph_rect[3]*0.5-4))
                
                if market_analysis_surface is None:
                    raise Exception("After plotting the mean price on the market_analysis_surface it suddenly became None")

                
                #calculating the span of the y_axis and the x_axis. The y_axis is special because it needs to be same scale on
                #both sellers and buyers side, even if one is entirely empty. That's the reason for the 'sell_offers_have_higher_span'
                if max_price - market_price > market_price - min_price:
                    sell_offers_have_higher_span = True
                    ylim = (- max_price + 2 * market_price, max_price) 
                else:    
                    sell_offers_have_higher_span = False
                    ylim = (min_price,market_price * 2 - min_price)

                
                xlim = (0,max_quantity)
                if ylim[0] == ylim[1]:
                    ylim = (ylim[0]-1,ylim[1]+1)
                y_position_here = self.frame_size
                self.positional_database = {"bidding_mode":{},"non_bidding_mode":{}}
                self.positional_database["bidding_mode"]["price"] = ylim
                self.positional_database["bidding_mode"]["quantity"] = xlim
                
                #plotting all data points. The reason it is divided by _next, _here, and _before is that it is faster to make a positional database that way
                # ie. to delineate where a click reacts to what. In sparse plots it is okay with plenty of imprecision, but if there are many bids the precision in clicking is of course
                #required to be higher
                for i in range(0,len(prices)):
                    
                    plotting_area_height = self.graph_rect[3] - self.frame_size * 2 - self.blank_area_in_middle_height
                    y_position_before = y_position_here
                    if i == 0:
                        y_position_here = (self.graph_rect[3] - self.frame_size) - (((prices[i] - ylim[0]) / ( ylim[1] - ylim[0])) * plotting_area_height )
                    else:
                        y_position_here = y_position_next
                    
                    if i == len(prices)-1:
                        y_position_next = self.graph_rect[3] - self.frame_size
                    else:
                        y_position_next = (self.graph_rect[3] - self.frame_size) - (((prices[i+1] - ylim[0]) / ( ylim[1] - ylim[0])) * plotting_area_height )
                    
                    x_length = int((self.graph_rect[3]) * math.log10(quantities[i]) / math.log10(xlim[1]) ) 
                    
                    if ((prices[i] - ylim[0]) / ( ylim[1] - ylim[0])) > 0.5: #ie if this is a sell offer
                        y_position_here = y_position_here - self.blank_area_in_middle_height
                    pygame.draw.line(market_analysis_surface,(50,50,50),(0,y_position_here),(x_length,y_position_here))
                    
                    #making positional database for linking clicking on the graph
                    max_width_of_selection_area = 10
                    top_border_length = min((y_position_here - y_position_before)/2,max_width_of_selection_area)
                    bottom_border_length = min((y_position_next - y_position_here)/2,max_width_of_selection_area)
                    top_border = y_position_here - top_border_length + self.graph_rect[1]
                    height = top_border_length + bottom_border_length
                    if height == 0: height = 1
                    left_border = self.graph_rect[0]
                    width = x_length
                    #debugging_info = "exact y_pos: " + str(y_position_here + self.rect[1] + 21) + " top border: +" + str(top_border_length) + " bottom border: -" + str(bottom_border_length) 
                    self.positional_database["non_bidding_mode"][(left_border,top_border,width,height)] = {"linkto":provider[i],"text":provider[i].name + ": " + "%.5g" % prices[i],"figure":((left_border,y_position_here + self.graph_rect[1]),(left_border + width,y_position_here + self.graph_rect[1]))}
                
                
                #making x-axis scale
                x_axis_vertical_position_percent_of_frame = 0.9 # in percent of lower frame where 1 is at top of frame
                x_axis_vertical_position = self.graph_rect[3]-int(self.frame_size*x_axis_vertical_position_percent_of_frame)
                pygame.draw.line(market_analysis_surface,(0,0,0),(0,x_axis_vertical_position),(self.graph_rect[2],x_axis_vertical_position),3)
                pygame.draw.line(market_analysis_surface,(0,0,0),(0,self.graph_rect[3] - x_axis_vertical_position),(self.graph_rect[2],self.graph_rect[3] - x_axis_vertical_position),3)
                pygame.draw.line(market_analysis_surface,(0,0,0),(0,x_axis_vertical_position),(0,self.graph_rect[3] - x_axis_vertical_position),3)
                pygame.draw.line(market_analysis_surface,(0,0,0),(self.graph_rect[2],x_axis_vertical_position),(self.graph_rect[2],self.graph_rect[3] - x_axis_vertical_position),3)
                max_x_axis_mark = 10 ** math.floor(math.log10(max_quantity)) #the value of the maximal x-axis mark. If eg. max_quantity is 1021, the max_x_axis_mark is 10^4
                if (max_quantity / max_x_axis_mark) < 6: # because then there is no room for the "units" marker
                    max_x_axis_mark = max_x_axis_mark / 10
                max_x_axis_mark_pos = int((self.graph_rect[3]) * math.log10(max_x_axis_mark) / math.log10(xlim[1]) )
                mark_height = self.graph_rect[3] / 50
                for i in range(0,10): #iterating "downwards" so to speak, because the x_mark_line will give the lineage of 10fold lower marks
                    x_mark_here = int(max_x_axis_mark / (10**i))
                    if x_mark_here < 10: #we stop the show at 10
                        break
                    x_pos_here = int((self.graph_rect[3]) * math.log10(x_mark_here) / math.log10(xlim[1]) )
                    pygame.draw.line(market_analysis_surface,(0,0,0),(x_pos_here,x_axis_vertical_position + mark_height/2),(x_pos_here,x_axis_vertical_position - mark_height/2))
                    x_mark_label_text = "10^"+str(int(math.log10(x_mark_here)))
                    if i == 0:
                        x_mark_label_text = x_mark_label_text + " units"  
                    x_mark_label = global_variables.standard_font.render(x_mark_label_text,True,(0,0,0))
                    market_analysis_surface.blit(x_mark_label,(x_pos_here-self.graph_rect[2]/100,x_axis_vertical_position + (mark_height)))
                    if market_analysis_surface is None:
                        raise Exception("At the end of the market_analysis_surface section, the surface had become None")
                
        return market_analysis_surface
                
        

            


    def update_data_history(self):
        history_surface = pygame.Surface((self.graph_rect[2],self.graph_rect[3]))
        history_surface.fill((212,212,212))
        resource = self.resource_selected

        #determining which market to look at. If in base mode it is obvious which. In firm for non-merchants it is home city, and for merchant it should be selectable
        if self.solar_system_object_link.display_mode == "base":
            market = self.solar_system_object_link.current_planet.current_base.market
        elif self.solar_system_object_link.display_mode == "firm":
            firm_selected = self.solar_system_object_link.firm_selected
            if isinstance(firm_selected, company.merchant):
                market = self.base_selected_for_merchant.market
            else:
                market = firm_selected.location.market
        else:
            raise Exception("The display mode " + str(self.solar_system_object_link.display_mode) + " is not supposed to show market data")

        if len(market["transactions"][resource])==0:
            no_history_label = global_variables.standard_font.render("No " + resource + " sold on market",True,(0,0,0))
            history_surface.blit(no_history_label,(0,self.graph_rect[3]*0.5-4))
        else:
            start_date = market["transactions"][resource][0]["date"]
            end_date = market["transactions"][resource][-1]["date"]
            relative_numeric_start_date = (start_date - self.solar_system_object_link.start_date).days
            relative_numeric_end_date = (end_date - self.solar_system_object_link.start_date).days
            xlim = (relative_numeric_start_date,relative_numeric_end_date)
            dates = []
            price = []
            quantity = []
            seller = []
            buyer = []
            for transaction in market["transactions"][resource]:
                dates.append((transaction["date"] - self.solar_system_object_link.start_date).days)
                price.append(transaction["price"])
                quantity.append(transaction["quantity"])
                seller.append(transaction["seller"])
                buyer.append(transaction["buyer"])
            ylim = (0,max(price))
            if ylim[0] == ylim[1]:
                ylim = (ylim[0]-1,ylim[1]+1)
            if xlim[0] == xlim[1]:
                xlim = (xlim[0]-1,xlim[1]+1)
            
            history_surface = primitives.make_linear_y_axis(history_surface, self.frame_size, ylim, self.solar_system_object_link, unit ="price")
            history_surface = primitives.make_linear_x_axis(history_surface, self.frame_size, xlim, solar_system_object_link = self.solar_system_object_link, unit = "date")
            
            
            self.positional_database = {"bidding_mode":{},"non_bidding_mode":{}}
            self.positional_database["bidding_mode"]["price"] = ylim
            
            for i in range(0,len(price)):
                x_position = int(self.frame_size + ((self.graph_rect[2]-self.frame_size*2) * (dates[i] - xlim[0])) / (xlim[1]-xlim[0]))
                y_position = int(self.graph_rect[3] - (self.frame_size + ( (self.graph_rect[3]-self.frame_size*2) * (price[i] - ylim[0]) / (ylim[1]-ylim[0]) )))
                try: dot_size = int(math.log10(quantity[i]))
                except:
                    print "DEBUGGING WARNING: quantity in a depicted transaction was " + str(quantity[i]) + " and this made the log function crash. You should probably look into the market functions and investigate why some bids are 0 or negative"
                    print "all quantities: " + str(quantity)
                    dot_size = 1
                pygame.draw.circle(history_surface,(0,0,0),(x_position,y_position),dot_size)
                
                
                left_border = x_position + self.graph_rect[0] - dot_size
                top_border = y_position + self.graph_rect[1] - dot_size 
                if seller[i] is not None and buyer[i] is not None: #can happen with the empty startup transactions
                    self.positional_database["non_bidding_mode"][(left_border,top_border,2*dot_size,2*dot_size)] = {"linkto":seller[i],"text":str(seller[i].name) + " to " + str(buyer[i].name) + ": 10^" + str(dot_size) + "units","figure":((dot_size),(x_position + self.graph_rect[0],y_position + self.graph_rect[1])),"debug":left_border- dot_size}

            if len(price) != len(quantity) or len(price) != len(dates):
                raise Exception("DEBUGGING WARNING: There is a problem with unequal length in the markethistoryplotter")
                    
        return(history_surface)





    def make_manual_bid(self,initial_price = None,initial_quantity = None):
        """
        Function that will give the player the option to place a manual bid.
        First pre-selected parameters for resource-choice, initial choice and range of price, intial choice and range of quantity
        #transaction-direction (buy or sell), and for location choices (for merchants) are choosen. 
        """
        
        self.graph_selected = "place bid mode"
        print "at start of function"
        print "initial_quantity: " + str(initial_quantity)
        print "initial_price: " + str(initial_price)
        #
        resource = self.resource_selected
        
        if self.solar_system_object_link.display_mode == "base":
            firm_selected = self.solar_system_object_link.current_planet.current_base
        elif self.solar_system_object_link.display_mode == "firm":
            firm_selected = self.solar_system_object_link.firm_selected
        else:
            raise Exception("The display mode " + str(self.solar_system_object_link.display_mode) + " is not supposed to show market data")
        
        

        
        #seller or buyer
        if isinstance(firm_selected, company.merchant): 
            if self.base_selected_for_merchant == firm_selected.from_location:
                direction = "buy"
            else:
                direction = "sell"
        elif resource in firm_selected.input_output_dict["input"]:
            direction = "buy"
        elif resource in firm_selected.input_output_dict["output"]:
            direction = "sell"
        else:
            raise Exception("Oddly the resource " + str(resource) + " was neither found in the input or output of " + str(firm_selected.name)) 
        
        
        
        if direction == "sell": #in this case we are mostly interested in the stock
            #sell quantity
            if isinstance(firm_selected, company.merchant):
                if self.base_selected_for_merchant == firm_selected.from_location:
                    quantity_max = firm_selected.from_stock_dict[resource]
                elif self.base_selected_for_merchant == firm_selected.to_location:
                    quantity_max = firm_selected.to_stock_dict[resource]
                else:
                    raise Exception("The self.base_selected_for_merchant " + str(self.base_selected_for_merchant.name) + " was neither in the from or the to_location of " + str(firm_selected.name))
            else:
                quantity_max = firm_selected.stock_dict[resource]
                

        else:
            #buy quantity
            if isinstance(firm_selected, company.merchant):
                print "NEED TO SET quantity range for a merchant. Defaulting to 100"
                quantity_max = 100
            else:
                print dir(firm_selected)
                print firm_selected.input_output_dict
                quantity_max = firm_selected.input_output_dict["input"][resource] * 10


        quantity_range = (0,quantity_max)
        if initial_quantity is None:
            initial_quantity = quantity_max
        else:
            initial_quantity = min(quantity_range[1], initial_quantity)
            
        #price setting
        if isinstance(firm_selected, company.merchant):
            market = self.base_selected_for_merchant.market
        else:
            market = firm_selected.location.market
            
        if len(market["buy_offers"][resource]) > 0:
            max_price = market["buy_offers"][resource][0]["price"]
        else:
            max_price = 10
        for transaction in market["transactions"][resource]:
            max_price = max(max_price, transaction["price"])
        print "max_price: " + str(max_price)
            
        price_range = (0,int(max_price * 2))
        if initial_price is None:
            initial_price = max_price
                
        
        print "initial_quantity: " + str(initial_quantity)
        print "quantity_range: " + str(quantity_range)
        print "initial_price: " + str(initial_price)
        print "price_range: " + str(price_range)
        
        
        pygame.draw.rect(self.action_surface,(212,212,212),self.graph_rect)
        height_to_draw = 10
        
        
        
        #row 1 set the price
        fixed_price_text = global_variables.standard_font.render("Set the price:",True,(0,0,0))
        self.action_surface.blit(fixed_price_text, (self.graph_rect[0], self.graph_rect[1] + height_to_draw))
        price_rect = pygame.Rect(self.graph_rect[0] + fixed_price_text.get_width(), self.graph_rect[1] + height_to_draw,self.graph_rect[2] - fixed_price_text.get_width(),fixed_price_text.get_height())
        variable_price_text = global_variables.standard_font.render(str(int(initial_price)),True,(0,0,0))
        self.action_surface.blit(variable_price_text, (price_rect[0], price_rect[1]))
        
        
        def price_execute(label, price_rect):
            pygame.draw.rect(self.action_surface,(212,212,212),price_rect)
            variable_price_text = global_variables.standard_font.render(str(self.price_bar.position),True,(0,0,0))
            self.action_surface.blit(variable_price_text, (price_rect[0], price_rect[1]))
            pygame.display.update(price_rect)
            


        self.price_bar = gui_components.hscrollbar(self.action_surface, 
                                  price_execute, 
                                  (self.graph_rect[0] + 10, self.graph_rect[1] + height_to_draw + 20), 
                                  self.graph_rect[2]-20, 
                                  price_range, 
                                  start_position = int(initial_price), 
                                  function_parameter=price_rect)



        #row 2 set the quantity
        height_to_draw = height_to_draw + 60
        
        fixed_quantity_text = global_variables.standard_font.render("Set the quantity:",True,(0,0,0))
        self.action_surface.blit(fixed_quantity_text, (self.graph_rect[0], self.graph_rect[1] + height_to_draw))
        quantity_rect = pygame.Rect(self.graph_rect[0] + fixed_quantity_text.get_width(), self.graph_rect[1] + height_to_draw,self.graph_rect[2] - fixed_quantity_text.get_width(),fixed_quantity_text.get_height())
        variable_quantity_text = global_variables.standard_font.render(str(initial_quantity),True,(0,0,0))
        self.action_surface.blit(variable_quantity_text, (quantity_rect[0], quantity_rect[1]))
        

        
        def quantity_execute(label, quantity_rect):
            pygame.draw.rect(self.action_surface,(212,212,212),quantity_rect)
            variable_quantity_text = global_variables.standard_font.render(str(self.quantity_bar.position),True,(0,0,0))
            self.action_surface.blit(variable_quantity_text, (quantity_rect[0], quantity_rect[1]))
            pygame.display.update(quantity_rect)

        self.quantity_bar = gui_components.hscrollbar(self.action_surface, 
                                  quantity_execute, 
                                  (self.graph_rect[0] + 10, self.graph_rect[1] + height_to_draw + 20), 
                                  self.graph_rect[2]-10, 
                                  quantity_range, 
                                  start_position = initial_quantity, 
                                  function_parameter=quantity_rect)


        

        
        #row 3: direction info
        height_to_draw = height_to_draw + 50
        direction_text  = global_variables.standard_font.render("Transaction type:",True,(0,0,0))
        self.action_surface.blit(direction_text, (self.graph_rect[0], self.graph_rect[1] + height_to_draw))
        
        def direction_execute(label, function_parameter):
            print "direction"
            print label
            print function_parameter
            
        
        self.direction_buttons = gui_components.radiobuttons(["buy","sell"],
                                   self.action_surface, 
                                   direction_execute,
                                   function_parameter = None, 
                                   topleft = (self.graph_rect[0] + 10, self.graph_rect[1] + height_to_draw + 20), 
                                   selected = direction)
        
        


        
        #row 4: show location
#        height_to_draw = height_to_draw + 50
#        
#        location_text = global_variables.standard_font.render("Set the location:",True,(0,0,0))
#        self.action_surface.blit(location_text, (self.graph_rect[0], self.graph_rect[1] + height_to_draw))
#
#        
#        def location_execute(label, function_parameter):
#                print "location"
#                print label
#                print function_parameter
#
#        if isinstance(firm_selected, company.merchant): 
#            self.location_buttons = gui_components.radiobuttons([firm_selected.from_location.name,firm_selected.to_location.name],
#                           self.action_surface, 
#                           direction_execute,
#                           function_parameter = None, 
#                           topleft = (self.graph_rect[0] + 10, self.graph_rect[1] + height_to_draw + 20), 
#                           selected = None)
#        else:
#                        self.location_buttons = gui_components.radiobuttons([firm_selected.location.name],
#                           self.action_surface, 
#                           direction_execute,
#                           function_parameter = None, 
#                           topleft = (self.graph_rect[0] + 10, self.graph_rect[1] + height_to_draw + 20), 
#                           selected = None)
        
        #effectuate buttons
        self.ok_button = gui_components.button("ok", 
                                                self.action_surface,
                                                self.effectuate_market_bid, 
                                                function_parameter = market, 
                                                fixed_size = (100,35), 
                                                topleft = (self.graph_rect[0] + self.graph_rect[2] - 110, self.graph_rect[1] + self.graph_rect[3] - 40)
                                                )


        


    def effectuate_market_bid(self, label, market):
        """
        Function that will check if the given numbers are ok, and if so effectuate the market bid
        """
        
#        all_ok = True
        if self.solar_system_object_link.display_mode == "base":
            firm_selected = self.solar_system_object_link.current_planet.current_base
        elif self.solar_system_object_link.display_mode == "firm":
            firm_selected = self.solar_system_object_link.firm_selected
        else:
            raise Exception("The display mode " + str(self.solar_system_object_link.display_mode) + " is not supposed to show market data")
        price = self.price_bar.position
        quantity = self.quantity_bar.position
        
        #determining direction
        direction = self.direction_buttons.selected

        
        #determining market
#        if isinstance(firm_selected, company.merchant): 
#            if self.bid_window.grid[(3,1)].active:
#                market = firm_selected.from_location.market
#            elif self.bid_window.grid[(3,2)].active:
#                market = firm_selected.to_location.market
#            else:
#                all_ok = False
#                if self.solar_system_object_link.message_printing["debugging"]:
#                    print_dict = {"text":"DEBUGGING: no market was selected","type":"debugging"}
#                    self.solar_system_object_link.messages.append(print_dict)
#                    self.manager.emit("update_infobox", None)
#        else:
#            market = firm_selected.location.market

        
        #determining resource
        resource = self.resource_selected
#        if isinstance(firm_selected, company.merchant):
#            if self.bid_window.grid[(4,1)].active:
#                resource = firm_selected.resource
#            elif self.bid_window.grid[(4,2)].active:
#                resource = firm_selected.transport_type
#            else:
#                all_ok = False
#                if self.solar_system_object_link.message_printing["debugging"]:
#                    print_dict = {"text":"DEBUGGING: no resource was selected","type":"debugging"}
#                    self.solar_system_object_link.messages.append(print_dict)
#                    self.manager.emit("update_infobox", None)
#            
#        else:
#            resource = self.bid_window.grid[(4,1)].text
        
        
        
        
#        if direction not in ["sell","buy"]:
#            if self.solar_system_object_link.message_printing["debugging"]:
#                print_dict = {"text":"The direction " + str(direction) + " was not recognized. Must be sell or buy","type":"debugging"}
#                self.solar_system_object_link.messages.append(print_dict)
#                self.manager.emit("update_infobox", None)
#            all_ok = False

#        try:    float(price)
#        except:
#            print_dict = {"text":"The price " + str(price) + " could not be converted into a decimal number. Please use another.","type":"general gameplay info"}
#            self.solar_system_object_link.messages.append(print_dict)
#            all_ok = False
#        else:
#            pass
        
#        
#        try:    int(quantity)
#        except:
#            print_dict = {"text":"The quantity " + str(quantity) + " could not be converted into an integer number. Please use another.","type":"general gameplay info"}
#            self.solar_system_object_link.messages.append(print_dict)
#            self.manager.emit("update_infobox", None)
#            all_ok = False
#        else:
#            pass
#        
#        if isinstance(firm_selected, company.merchant): #then we need to see see if it buys in the from location or to location
        
#        if all_ok:
#            self.exit()
        if direction == "buy":
            own_offer = {"resource":resource,"price":float(price),"buyer":firm_selected,"name":firm_selected.name,"quantity":int(quantity),"date":self.solar_system_object_link.current_date}
        elif direction == "sell":
            own_offer = {"resource":resource,"price":float(price),"seller":firm_selected,"name":firm_selected.name,"quantity":int(quantity),"date":self.solar_system_object_link.current_date}
        else:
            raise Exception("Unknown direction " + str(direction))
        
        firm_selected.make_market_bid(market,own_offer)
        
        print_dict = {"text":firm_selected.name + " succesfully made a " + str(direction) + " bid for " + str(quantity) + " units of " + str(resource) + " at price " + str(price),"type":"general gameplay info"}
        self.solar_system_object_link.messages.append(print_dict)
        self.graph_selected = "market bids"
        return "clear"
#        self.manager.emit("update_infobox", None)
#        self.create_base_and_firm_market_window(self.renderer)


                    


        
    def receive_click(self,event):
        """
        Function that will take the position of a mouse click and check if any market-window variables (either history or market bids)
        are present at that position. If so, it will highlight these with further info on first click and provide a link on second click
        """ 
        #transposing position to take the main window rect into account

        position = event.pos
        if self.graph_rect.collidepoint(position) == 1:
            if self.graph_selected == "place bid mode": #if we are in bidding mode
                
                if self.price_bar.rect.collidepoint(position) == 1:
                    self.price_bar.activate(position)
                if self.quantity_bar.rect.collidepoint(position) == 1:
                    self.quantity_bar.activate(position)
                if self.direction_buttons.rect.collidepoint(position) == 1:
                    self.direction_buttons.activate(position)
                if self.ok_button.rect.collidepoint(position) == 1:
                    return self.ok_button.activate(position)


            
            
            else: #if we are in history or market mode
                if self.bidding_mode: #if the graphs accept bids we start the bidding sections up
                    print "the graph will now accept your bid"
                    if self.graph_selected == "market bids":
                        top_of_plot = self.rect[1] + self.frame_size  + 21
                        self.blank_area_in_middle_height
                        y_position =  position[1] - top_of_plot
                        if y_position > (self.graph_rect[3] - 2 * self.frame_size) / 2 + self.blank_area_in_middle_height/2:
                            y_position = y_position - self.blank_area_in_middle_height #more than half - correct and move on
                        elif y_position > (self.graph_rect[3] - 2 * self.frame_size) / 2 - self.blank_area_in_middle_height/2:
                            return None #Hit half - don't continue
                        height_of_plot = self.graph_rect[3] - 2 * self.frame_size - self.blank_area_in_middle_height 
                        y_relative_position = 1.0 - (y_position / float(height_of_plot))
                    else: #in history graph
                        y_relative_position =  ((self.graph_rect[3] - self.frame_size) - (position[1] - self.rect[1] - 21)) / float(self.graph_rect[3] - self.frame_size)
        
        
                    
        
                    x_relative_position =  (position[0] - self.rect[0] - 150) / float(self.graph_rect[2])
                    if 0 < x_relative_position < 1:
                        if 0 < y_relative_position < 1:
                            if "price" in self.positional_database["bidding_mode"].keys():
                                min_price = self.positional_database["bidding_mode"]["price"][0]
                                max_price = self.positional_database["bidding_mode"]["price"][1]
                                price = y_relative_position * (max_price - min_price) + min_price
                                if price < 0:
                                    print "Changed price from " + str(price) + " to 0"
                                    price = 0

                            else:
                                price = None
                                
                            if "quantity" in self.positional_database["bidding_mode"].keys():
                                max_qt = self.positional_database["bidding_mode"]["quantity"][1]
                                try:    math.log10(max_qt)
                                except: 
                                    print "DEBUGGING: no good selection of log10 max_qt"
                                    quantity = None
                                else:
                                    quantity = int(10 ** (math.log10(max_qt) * x_relative_position))  
                            else:
                                quantity = None
                        
                            print "click at " + str((x_relative_position,y_relative_position)) + " gives price: " + str(price) + " and qt: " + str(quantity)
                            self.make_manual_bid(price,quantity)
                                
    
                else:  #if the graphs do not accept bids we only display some information
                    click_spot = pygame.Rect(position[0]-1,position[1]-1 ,2,2)
                    click_spot_result = click_spot.collidedict(self.positional_database["non_bidding_mode"])
                    if click_spot_result is not None:
                        if event.button == 3:
                            if not isinstance(click_spot_result[1]["linkto"],company.base): #if it was a base there would be no point, since it would already in zoom
                                linkto = click_spot_result[1]["linkto"]
                                if isinstance(linkto, company.base):
                                    self.solar_system_object_link.display_mode = "base"
                                    self.solar_system_object_link.current_planet.current_base = linkto
                                elif isinstance(linkto, company.firm) or isinstance(linkto, company.merchant) or isinstance(linkto, company.research):
                                    self.solar_system_object_link.display_mode = "firm"
                                    self.solar_system_object_link.firm_selected = linkto
                                else:
                                    raise Exception("The class of " + linkto.name + " was " + linkto.__class__)
                                return "clear"
                        else:
                            self.highlighted_transactions.append(click_spot_result[1])
                            
                            text_size = global_variables.standard_font_small.size(click_spot_result[1]["text"]) 
                            text = global_variables.standard_font_small.render(click_spot_result[1]["text"],True,(0,0,0))
                            
                            text_position = (click_spot_result[1]["figure"][1][0]-text_size[0] / 2,click_spot_result[1]["figure"][1][1])
                            
                            if text_position[0] < self.graph_rect[0] + self.frame_size:
                                text_position = (self.graph_rect[0] + self.frame_size, text_position[1])
                            if text_position[0] + text_size[0] > self.graph_rect[0] + self.graph_rect[2]:
                                text_position = (self.graph_rect[0] + self.graph_rect[2] - text_size[0], text_position[1])

                            
                            self.action_surface.blit(text,text_position)
                            
                            if self.graph_selected == "market bids":
                                pygame.draw.line(self.action_surface,(100,100,255),click_spot_result[1]["figure"][0],click_spot_result[1]["figure"][1])
                            elif self.graph_selected == "history":
                                pygame.draw.circle(self.action_surface,(100,100,255),click_spot_result[1]["figure"][1],click_spot_result[1]["figure"][0])
                            else:
                                raise Exception("Unknown graph type " + self.graph_selected)
        
                            pygame.display.flip()


                            
        else: #if the click is elsewhere than the graph window
            if self.graph_selected != "place bid mode":
                if self.update_button.rect.collidepoint(event.pos) == 1:
                    self.update_button.activate(event.pos)
                if self.resource_buttons.rect.collidepoint(event.pos) == 1:
                    self.resource_buttons.activate(event.pos)
                if self.graph_buttons.rect.collidepoint(event.pos) == 1:
                    self.graph_buttons.activate(event.pos)
                if "activate" in dir(self.market_selection_buttons):
                    if self.market_selection_buttons.rect.collidepoint(event.pos) == 1:
                        self.market_selection_buttons.activate(event.pos)
                if "activate" in dir(self.bid_button):
                    if self.bid_button.rect.collidepoint(event.pos) == 1:
                        self.bid_button.activate(event.pos)
            
            
            
                    
            



class base_build_menu():
    """
    Subview of the base view. Shows all options regarding building firms and other bases from the current base.
    
    The first list is derived from the list of currently known technologies + options to build research, merchants and new bases.
    
    The actions from choosing a commodity producer from the known technologies is to create that firm in the current city. Likewise, more
    or less, for research firms. Choosing merchant brings up question boxes about where the destination and what resource should be traded.
    Choosing new base building brings zooms out to base position mode.
    
    
    """

    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface
        
        self.menu_position = "root"
        self.selections = {}
        self.text_receiver = None


#    def exit(self, label, function_parameter):
#        return "clear"

    def create(self):
        """
        The creation function.  
        """
        self.menu_position = "root"
        self.selections = {}
        

        buildoption_data = {}
        for technology_name in self.solar_system_object_link.current_player.known_technologies:
            if technology_name != "common knowledge":
                technology = self.solar_system_object_link.current_player.known_technologies[technology_name]
            
                buildoption_data[technology_name] = {}
                
                
                #nicefying input output
                nice_input_output_line = ""
                for put in ["input","output"]:
                    if put == "output":
                        nice_input_output_line = nice_input_output_line + "-> "
                    for resource in technology["input_output_dict"][put].keys():
                        value = technology["input_output_dict"][put][resource]
                        nice_input_output_line = nice_input_output_line + resource + ": " + str(value) + " "
                        
                buildoption_data[technology_name]["input and output"] = str(nice_input_output_line)
                
    

        buildoption_data["research"] = {}
        buildoption_data["research"]["input and output"] = "labor: 1 -> research points"

        buildoption_data["merchant"] = {}
        buildoption_data["merchant"]["input and output"] = "transport: 1 -> movement of goods"

        buildoption_data["new base"] = {}
        buildoption_data["new base"]["input and output"] = "population: 100 steel: 100 labor: 100 -> new base"
        
        self.fast_list = gui_components.fast_list(self.action_surface, buildoption_data, rect = self.rect)


    def receive_click(self,event):
        
        if event.button == 1:
            if self.menu_position == "pick name":
                if self.ok_button.rect.collidepoint(event.pos) == 1:
                    self.ok_button.activate(event)
                    return "clear"
            elif self.menu_position == "commodity size":
                if self.slider.rect.collidepoint(event.pos) == 1:
                    self.slider.activate(event.pos)
                if self.ok_button.rect.collidepoint(event.pos) == 1:
                    return self.ok_button.activate(event.pos)
            
            elif self.menu_position == "commodity name":
                if self.ok_button.rect.collidepoint(event.pos) == 1:
                    self.ok_button.activate(event.pos)
                    return "clear"
                    
                
            else:
                self.fast_list.receive_click(event)
        
        
        if event.button == 3:
            self.fast_list.receive_click(event)
            if self.menu_position == "root":
                if self.fast_list.selected_name is not None:
                    if self.fast_list.selected_name == "merchant":
                        self.merchant_pick_destination()
                    elif self.fast_list.selected_name == "new base":
                        return "new base"
                    else:
                        self.commodity_size_selection(self.fast_list.selected_name)
            
            elif self.menu_position == "pick destination":
                if self.fast_list.selected_name is not None:
                    self.merchant_pick_resource(self.fast_list.selected_name)
            
            elif self.menu_position == "pick resource":
                if self.fast_list.selected_name is not None:
                    self.merchant_pick_name(self.fast_list.selected_name)
                    
                





  
    def merchant_pick_destination(self):
        """
        Function to ask what destination the merchant should trade with
        """
        self.menu_position = "pick destination"
        destination_data = {}
        location = self.solar_system_object_link.current_planet.current_base
        for destination_name in location.trade_routes:
            destination = location.trade_routes[destination_name]
            
            destination_data[destination_name] = {}
            destination_data[destination_name]["distance"] = destination["distance"]
            destination_data[destination_name]["type"] = destination["transport_type"]

        self.fast_list = gui_components.fast_list(self.action_surface, destination_data, rect = self.rect)

            
            
        
    def merchant_pick_resource(self, destination_name):
        """
        Function to ask what resource the merchant should trade in
        """
        self.menu_position = "pick resource"
        

        from_location = self.solar_system_object_link.current_planet.current_base
        trade_route_selected = from_location.trade_routes[destination_name]
    
        #prepare direct links to the other endpoint location
        for endpoint in trade_route_selected["endpoint_links"]:
            if endpoint != from_location:
                to_location = endpoint
        
        #prepare resource data
        resource_data = {}
        for resource in self.solar_system_object_link.trade_resources.keys():
            if self.solar_system_object_link.trade_resources[resource]["transportable"]:
                resource_data[resource] = {}
                
                quantity_offered_here = 0
                prices = []
                for sell_offer in from_location.market["sell_offers"][resource]:
                    quantity_offered_here = quantity_offered_here + sell_offer["quantity"]
                    prices.append(sell_offer["price"])
                if len(prices) == 0:
                    cheapest_sell_price = None
                else:
                    cheapest_sell_price = min(prices)
                    
                if len(to_location.market["buy_offers"][resource]) > 0:
                    best_buy_price = to_location.market["buy_offers"][resource][0]["price"]
                else:
                    best_buy_price = None
                
                resource_data[resource]["Qt on market here"] = quantity_offered_here
                resource_data[resource]["Best sell price"] = cheapest_sell_price
                resource_data[resource]["Best buy price"] = best_buy_price
            
        self.fast_list = gui_components.fast_list(self.action_surface, resource_data, rect = self.rect)    
        
        
        
        
        
        from_location = self.solar_system_object_link.current_planet.current_base
        trade_route_selected = from_location.trade_routes[destination_name]
        for endpoint in trade_route_selected["endpoint_links"]:
            if endpoint != from_location:
                to_location = endpoint
        self.selections = {"to_location":to_location,"from_location":from_location,"trade_route_selected":trade_route_selected}


    def merchant_pick_name(self,resource,give_length_warning=False):
        """
        Function to get the name of the merchant
        give_length_warning         If true, this will specify the max text size as part of the title.
        """
        self.menu_position = "pick name"
        
        self.selections["resource"] = resource


        #check that this does not already exist
        exists = False
        for firm_instance in self.solar_system_object_link.current_player.owned_firms.values():
            if isinstance(firm_instance, company.merchant):
                if firm_instance.from_location == self.selections["from_location"]:
                    if firm_instance.to_location == self.selections["to_location"]:
                        if firm_instance.resource == resource:
                            exists = True
        if exists:
            print_dict = {"text":"A merchant from " + str(self.selections["from_location"].name) + " to " + str(self.selections["to_location"].name) + " trading " + str(resource) + " does already exist","type":"general gameplay info"}
            self.solar_system_object_link.messages.append(print_dict)

            
        else:
            
            pygame.draw.rect(self.action_surface, (212,212,212), self.rect)
            pygame.draw.rect(self.action_surface, (0,0,0), self.rect, 2)
            pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0] + self.rect[2], self.rect[1]))
            pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0], self.rect[1] + self.rect[3]))

            text = global_variables.standard_font.render("Choose name for merchant:",True,(0,0,0))
            self.action_surface.blit(text, (self.rect[0] + 10, self.rect[1] + 10))

        
        
            if give_length_warning:
                warning = global_variables.standard_font.render("Name must be unique",True,(0,0,0))
                self.action_surface.blit(warning, (self.rect[0] + 10, self.rect[1] + 50))
                
                
            self.text_receiver = gui_components.entry(self.action_surface, 
                                 topleft = (self.rect[0] + 10, self.rect[1] + 90), 
                                 width = self.rect[3] - 20, 
                                 max_letters = global_variables.max_letters_in_company_names)
            self.text_receiver.active = True
    
            self.ok_button = gui_components.button("ok", 
                                                    self.action_surface,
                                                    self.merchant_build, 
                                                    function_parameter = None, 
                                                    fixed_size = (100,35), 
                                                    topleft = (self.rect[0] + 10, self.rect[1] + 150)
                                                    )
            

        
        
        
        
    def merchant_build(self,label,function_parameter):
        """
        Function to build the merchant
        """ 
        for test in ["to_location","from_location","trade_route_selected","resource"]:
            if test not in self.selections.keys():
                raise Exception("The " + test + " was not properly selected")
        
        resource = self.selections["resource"]
        
        
        name = self.text_receiver.text

        #test if name is unique
        unique = True
        for company_instance in self.solar_system_object_link.companies.values():
            if name in company_instance.owned_firms.keys():
                unique = False
        
        if 0 < len(name) <= global_variables.max_letters_in_company_names and unique:
            owner = self.solar_system_object_link.current_player
            input_output_dict = {"input":{},"output":{},"timeframe":30,"byproducts":{}}
            distance = self.selections["trade_route_selected"]["distance"]
            transport_type = self.selections["trade_route_selected"]["transport_type"]
            new_merchant_firm = company.merchant(self.solar_system_object_link,
                                                 self.selections["from_location"],
                                                 self.selections["to_location"],
                                                 input_output_dict,
                                                 owner,
                                                 name,
                                                 transport_type,
                                                 distance,
                                                 self.selections["resource"])
            owner.owned_firms[name] = new_merchant_firm
            print_dict = {"text":"Built a merchant named " + str(name) + " between " + str(self.selections["from_location"].name) + " and " + str(self.selections["to_location"].name) + " trading in " + str(self.selections["resource"]),"type":"general gameplay info"}
            self.solar_system_object_link.messages.append(print_dict)
            self.selections = {}
            self.menu_position = "root"
        else:
            print_dict = {"text":"the selected name " + str(name) + " was too long. Has to be less than " + str(global_variables.max_letters_in_company_names) + " characters","type":"general gameplay info"}
            self.solar_system_object_link.messages.append(print_dict)
            self.merchant_pick_name(self.selections["resource"],give_length_warning=True)


    
    def commodity_size_selection(self, company_type):
        """
        This function creates a dialog asking the size of the firm to be built
        The range of the size is from "1" where the it is just the input_output_dict
        to the integer at which the sum of the inputs are equal to 10% the population of the city (FIXME this rule is not implemented for AI - also note that it is more like 101% of the sum at present)
         
        """
        self.menu_position = "commodity size"
        
        if company_type in ["new base","merchant"]:
            raise Exception("This should have been distributed correctly already at the select_button_callback step")
        elif company_type == "research":
            technology = {}
            technology["input_output_dict"] = {}
            technology["input_output_dict"]["input"] = {"labor":1}
            technology["input_output_dict"]["output"] = {"research:":1}
            technology["technology_name"] = "research"
        else:
            technology = self.solar_system_object_link.current_player.known_technologies[company_type]
        
        input_size = 0
        
        
        #calculate the range allowed
        for input in technology["input_output_dict"]["input"].values():
            input_size = input_size + input
        if input_size < 2: 
            input_size = 2
        if self.solar_system_object_link.current_planet.current_base is None:
            raise Exception("very weird - there was no base selected")
        population = self.solar_system_object_link.current_planet.current_base.population
        max_size = int(population * 0.1 / float(input_size))
        
        
        #check if the current_player already owns a company of that technology in the current base
        existing_firm = None
        for firm_instance in self.solar_system_object_link.current_player.owned_firms.values():
            if firm_instance.location == self.solar_system_object_link.current_planet.current_base:
                if firm_instance.technology_name == company_type:
                    existing_firm = firm_instance
                    break
        
        
        #clean up the act
        pygame.draw.rect(self.action_surface, (212,212,212), self.rect)
        pygame.draw.rect(self.action_surface, (0,0,0), self.rect, 2)
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0] + self.rect[2], self.rect[1]))
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0], self.rect[1] + self.rect[3]))

        text = global_variables.standard_font.render("Choose size of firm:",True,(0,0,0))
        self.action_surface.blit(text, (self.rect[0] + 90, self.rect[1] + 10))

        
        
        if existing_firm is None:
            existing_firm_text = "No existing firms of this type owned here"
            start_value = 1
        else:
            existing_firm_text = "An existing size " + str(existing_firm.size) + " firm of this type already owned here. Choose size change?"
            start_value = existing_firm.size
  
        existing_firm_rendered_text = global_variables.standard_font_small.render(existing_firm_text,True,(0,0,0))
        self.action_surface.blit(existing_firm_rendered_text, (self.rect[0] + 130, self.rect[1] + 50))
        
        fastest = global_variables.standard_font.render("Smallest",True,(0,0,0))
        self.action_surface.blit(fastest, (self.rect[0] + 40, self.rect[1] + 40))

        slowest = global_variables.standard_font.render("Largest",True,(0,0,0))
        self.action_surface.blit(slowest, (self.rect[0] + 40, self.rect[1] + self.rect[3]-  50))
        
        
        def execute(label, technology):
            """
            This function is activated on scrollbar value change on the size selection box, and updates the input_output_dict
            """

            update_rect = pygame.Rect(self.rect[0] + 50, self.rect[1] + 70, self.rect[2] - 100, self.rect[3] - 150) 
            pygame.draw.rect(self.action_surface, (212,212,212), update_rect)
            
            size_info = global_variables.standard_font_small.render("size: " + str(self.slider.position),True,(0,0,0))
            self.action_surface.blit(size_info, (self.rect[0] + 130, self.rect[1] + 70))
            lineno = 0
            for put in ["input","output"]:
                lineno = lineno + 1
                direction_info = global_variables.standard_font_small.render(put+":",True,(0,0,0))
                self.action_surface.blit(direction_info, (self.rect[0] + 130, self.rect[1] + 70 + lineno * 20))
#                print technology.keys()
                for resource in technology["input_output_dict"][put].keys():
                    lineno = lineno + 1
                    value = technology["input_output_dict"][put][resource]
                    value = value * self.slider.position
#                    nice_input_output_line = nice_input_output_line +  + "\n"
                    value_info = global_variables.standard_font_small.render(resource + ": " + str(value),True,(0,0,0))
                    self.action_surface.blit(value_info, (self.rect[0] + 150, self.rect[1] + 70 + lineno * 20))



            
            
            self.ok_button = gui_components.button("ok", 
                                        self.action_surface,
                                        self.commodity_ask_for_name, 
                                        function_parameter = existing_firm, 
                                        fixed_size = (100,35), 
                                        topleft = (self.rect[0] + self.rect[2] - 110, self.rect[1] + self.rect[3] - 40))

            
            pygame.display.flip()
        
        self.slider = gui_components.vscrollbar (self.action_surface,
                                                execute,
                                                topleft = (self.rect[0] + 10, self.rect[1] + 30),
                                                length_of_bar_in_pixel = self.rect[3] - 60,
                                                range_of_values = (1,max_size),
                                                start_position = start_value,
                                                function_parameter = technology
                                                )
        execute(None,technology)
        
        self.selections = {"technology":technology} 
      


        
    def commodity_ask_for_name(self,label,existing_firm,give_length_warning=False):
        """
        This command is called after the size selection box has been accepted
        """
        size_requested = self.slider.position
        print "commodity_ask_for_name and existing_firm is " + str(existing_firm)
        self.menu_position = "commodity name"
        update_rect = pygame.Rect(self.rect[0] + 50, self.rect[1] + 70, self.rect[2] - 100, self.rect[3] - 150) 
        pygame.draw.rect(self.action_surface, (212,212,212), update_rect)

        
        if existing_firm is None:
            self.text_receiver = gui_components.entry(self.action_surface, 
                     topleft = (self.rect[0] + 50, self.rect[1] + 70, self.rect[2] - 100, self.rect[3] - 150), 
                     width = 300, 
                     max_letters = global_variables.max_letters_in_company_names)
            self.text_receiver.active = True
            self.ok_button = gui_components.button("ok", 
                self.action_surface,
                self.commodity_build_firm, 
                function_parameter = None, 
                fixed_size = (100,35), 
                topleft = (self.rect[0] + self.rect[2] - 110, self.rect[1] + self.rect[3] - 40))

        else: #in cases where the firm already exists, we preserve the name
             
            
            existing_info = global_variables.standard_font_small.render("Updating firm size",True,(0,0,0))
            self.action_surface.blit(existing_info, (self.rect[0] + 130, self.rect[1] + 70))
            pygame.display.flip()
            print "commodity_ask_for_name knows that existing firm is not none but " + str(existing_firm)
            self.commodity_build_firm(None, existing_firm)
            return "clear"


            
#            self.commodity_build_firm(technology, self.size_requested, existing_name = existing_firm.name)
            

        



    def commodity_build_firm(self,label,existing_firm):
        """
        The effectuating function for building commodity firms
        """
#        self.menu_position = "commodity build"
        
        if existing_firm is None:
            name = self.text_receiver.text
            
            unique = True
            for company_instance in self.solar_system_object_link.companies.values():
                if name in company_instance.owned_firms.keys():
                    unique = False
        
            if not (0 < len(name) <= global_variables.max_letters_in_company_names and unique):
                print_dict = {"text":"the selected name " + str(name) + " was too long and/or not unique. Has to be less than " + str(global_variables.max_letters_in_company_names) + " characters","type":"general gameplay info"}
                self.solar_system_object_link.messages.append(print_dict)

                self.commodity_ask_for_name(None,None,True)
                return None
            
        else: #if existing name exists, we use that
            name = existing_firm.name
        
        
        
        technology = self.selections["technology"]
        location = self.solar_system_object_link.current_planet.current_base
        owner = self.solar_system_object_link.current_player
        size = self.slider.position
        
        owner.change_firm_size(location,size,technology["technology_name"], name)
        if isinstance(name, str) or isinstance(name, unicode):
            print_dict = {"text":"Built a firm named " + str(name) + " at " + str(location.name) + " for " + str(owner.name),"type":"general gameplay info"}
            self.solar_system_object_link.messages.append(print_dict)

        else:
            print name
            print name.__class__
            raise Exception("The name used: " + str(name) + " was of class " + str(name.__class__) + " but should have been a string")
        




class company_ownership_info():
    """
    Subview of the company view. Shows miscellanous information about a company, such as decision parameters, capital and number of firms.
    """

    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface
        

    def receive_click(self,event):
        self.fast_list.receive_click(event)


        



    def create(self):
        """
        The creation function.  
        """
        company_selected = self.solar_system_object_link.company_selected
        if company_selected is not None:
            company_ownership_dict = {}
            
            for company_database_variable in company_selected.company_database:
                company_database_variable_name_here = company_database_variable
                if len(company_database_variable_name_here) > global_variables.max_letters_in_company_names:
                    company_database_variable_name_here = company_database_variable_name_here[0:global_variables.max_letters_in_company_names]
                company_ownership_dict["parameter: " + company_database_variable_name_here] = {"info":str(company_selected.company_database[company_database_variable])} 
            
            company_ownership_dict["capital"] = {"info":company_selected.capital}
           
            company_ownership_dict["home cities, number of"] = {"info":str(len(company_selected.home_cities))}
            if 0 < len(company_selected.home_cities) < 4:
                list_value = str(company_selected.home_cities.keys())
                list_value = list_value.rstrip("]")
                list_value = list_value.lstrip("[")
                company_ownership_dict["home cities"] = {"info":list_value}

            company_ownership_dict["last_firm_evaluation"] = {"info":str(company_selected.last_firm_evaluation)}
            company_ownership_dict["last_market_evaluation"] = {"info":str(company_selected.last_market_evaluation)}
            company_ownership_dict["last_demand_evaluation"] = {"info":str(company_selected.last_demand_evaluation)}
            company_ownership_dict["last_supply_evaluation"] = {"info":str(company_selected.last_supply_evaluation)}

            company_ownership_dict["research"] = {"info":str(company_selected.research)}    
            
            company_ownership_dict["firms owned, number of"] = {"info":str(len(company_selected.owned_firms))}

            self.fast_list = gui_components.fast_list(self.action_surface, company_ownership_dict, rect = self.rect)
        else:
            if self.solar_system_object_link.message_printing["debugging"]:
                print_dict = {"text":"DEBUGGING: Company selected was None","type":"debugging"}
                self.solar_system_object_link.messages.append(print_dict)








class company_financial_info():
    """
    Subview of the company view. Shows a graph of the capital of the company as it has been over the past years. 
    """


    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface

        self.graph_size = (self.rect[2], self.rect[3])
        self.frame_size = 80



    def create(self):
        """
        The creation function.  
        """
        
        company_selected = self.solar_system_object_link.company_selected
        company_accounting = company_selected.company_accounting
        history_surface = pygame.Surface(self.graph_size)
        history_surface.fill((234,228,223))
        pygame.draw.rect(self.action_surface, (0,0,0), self.rect, 2)
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0] + self.rect[2], self.rect[1]))
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0], self.rect[1] + self.rect[3]))
  
        
        if len(company_selected.company_accounting) == 0:
            no_history_label = global_variables.standard_font.render("No history for " + company_selected.name,True,(0,0,0))
            history_surface.blit(no_history_label,(20,20))
        else:
            start_date = company_accounting[0]["date"]
            end_date = company_accounting[len(company_accounting)-1]["date"]
            relative_numeric_start_date = (start_date - self.solar_system_object_link.start_date).days
            relative_numeric_end_date = (end_date - self.solar_system_object_link.start_date).days
            
            dates = []
            capital = []
            for account_report in company_accounting:
                dates.append((account_report["date"] - self.solar_system_object_link.start_date).days)
                capital.append(account_report["capital"])
                
            xlim = (min(dates),max(dates))
            ylim = (0,max(capital))
            if ylim[0] == ylim[1]:
                ylim = (ylim[0]-1,ylim[1]+1)
            if xlim[0] == xlim[1]:
                xlim = (xlim[0]-1,xlim[1]+1)
            
            
            history_surface = primitives.make_linear_y_axis(history_surface, self.frame_size, ylim, solar_system_object_link=self.solar_system_object_link, unit = "capital")
            history_surface = primitives.make_linear_x_axis(history_surface,self.frame_size,xlim, solar_system_object_link=self.solar_system_object_link, unit="date")
#            print "(self.graph_rect[2]-self.frame_size*2): " + str((self.graph_rect[2]-self.frame_size*2))
            for i in range(1,len(capital)):
                x1_position = int(self.frame_size + ((self.graph_rect[2]-self.frame_size*2) * (dates[i-1] - xlim[0])) / (xlim[1]-xlim[0]))
                y1_position = int(self.graph_rect[3] - (self.frame_size + ( (self.graph_rect[3]-self.frame_size*2) * (capital[i-1] - ylim[0]) / (ylim[1]-ylim[0]) )))
                x2_position = int(self.frame_size + ((self.graph_rect[2]-self.frame_size*2) * (dates[i] - xlim[0])) / (xlim[1]-xlim[0]))
                y2_position = int(self.graph_rect[3] - (self.frame_size + ( (self.graph_rect[3]-self.frame_size*2) * (capital[i] - ylim[0]) / (ylim[1]-ylim[0]) )))
#                print "From (" + str(x1_position) + "," + str(y1_position) + ") to (" + str(x2_position) + "," +str(y2_position) + ") - the date was: " + str(dates[i]) + " and the capital was " + str(capital[i])
                
                pygame.draw.line(history_surface,(0,0,0),(x1_position,y1_position),(x2_position,y2_position))
        
        
        self.action_surface.blit(history_surface,(self.rect[0],self.rect[1]))
        pygame.display.flip()



    def receive_click(self,event):
        print "Nothing should happen now"

class company_list_of_firms():
    """
    Subview of the company view. Shows a list of all firms owned by the company. A shortcut button allows quick zoom to the firm page of these firms.
    """

    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface
        


    def create(self):
        """
        The creation function.  
        """
        company_selected = self.solar_system_object_link.company_selected
        if company_selected is None:
            raise Exception("A list of firms was requested, but no company was selected")
        
        firm_data = {}
        for firm_instance in company_selected.owned_firms.values():
            firm_data[firm_instance.name] = {}
            try: firm_instance.last_profit
            except: 
                firm_data[firm_instance.name]["last profit"] = "NA"
            else: 
                firm_data[firm_instance.name]["last profit"] = firm_instance.last_profit
            
            firm_data[firm_instance.name]["location"] = firm_instance.location.name
            
            stock_amount = 0
            for stock_item in firm_instance.stock_dict.values():
                stock_amount = stock_amount + stock_item
            firm_data[firm_instance.name]["stock size"] = stock_amount
        self.fast_list = gui_components.fast_list(self.action_surface, firm_data, rect = self.rect)


    def receive_click(self,event):
        self.fast_list.receive_click(event)
        if event.button == 3:
            firm_selected = None
            for firm in self.solar_system_object_link.company_selected.owned_firms.values():
                if firm.name == self.fast_list.selected_name:
                    firm_selected = firm
            if firm_selected is None:
                if self.solar_system_object_link.message_printing["debugging"]:
                    print_dict = {"text":"POSSIBLE DEBUGGING: - the firm asked for was of None type","type":"debugging"}
                    self.solar_system_object_link.messages.append(print_dict)
    
            else:
                print "FIXME: Should go to firm window now"



class firm_trade_partners_info():
    """
    Subview of the firm view. Shows a list of past trading transactions for the firm.
    """
    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface
        


    def create(self):
        """
        The creation function. Doesn't return anything, but saves self.window_transactions variable and renders using the self.renderer. 
        """
        
        firm_selected = self.solar_system_object_link.firm_selected
        if isinstance(firm_selected,company.merchant):
            location_list = [firm_selected.from_location, firm_selected.to_location]
            
        else:
            location_list = [firm_selected.location]

        
        transactions = {}
        for k, location_instance in enumerate(location_list):
            market = location_instance.market
            for i, resource in enumerate(market["transactions"]):
                for j, transaction in enumerate(market["transactions"][resource]):
                    date = transaction["date"]
                    if transaction["buyer"] is not None:
                        buyer = transaction["buyer"].name
                    else:
                        buyer = None
                    if transaction["seller"] is not None:
                        seller = transaction["seller"].name
                    else:
                        seller = None
                    price = transaction["price"]
                    #print "The price is of class " + str(price.__class__)
                    quantity = transaction["quantity"]
                    if firm_selected.name in [buyer,seller]:
                        transactions[i*j*k] =  {"date":date,"buyer":buyer,"seller":seller,"price":price,"quantity":quantity}

        self.fast_list = gui_components.fast_list(
                                                  self.action_surface, 
                                                  transactions, 
                                                  rect = self.rect,
                                                  column_order = ["rownames","date","buyer","seller","price","quantity"])

    def receive_click(self,event):
        self.fast_list.receive_click(event)

        
        

class firm_process_info():
    """
    Subview of the firm view. Shows a list of the resources of interest for the firm. Both the stock and the production rate is shown.
    """

    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(50,50,700,500)
        self.action_surface = action_surface
        

        
    def receive_click(self,event):
        self.fast_list.receive_click(event)
            


    def create(self):
        """
        The creation function.  
        """
        
        firm_selected = self.solar_system_object_link.firm_selected
        
        
        if firm_selected is not None:
            
            if isinstance(firm_selected, company.merchant):
                process_and_stock_dict = {}
                for direction_name in ["destination","origin"]:
                    if direction_name == "destination":
                        base = firm_selected.to_location
                    else:
                        base = firm_selected.from_location
                    
                    direction = "in " + base.name
                    for resource in [firm_selected.resource, firm_selected.transport_type]:
                         process_and_stock_dict[resource + " at " + direction_name] = {}
                         process_and_stock_dict[resource + " at " + direction_name]["direction"] = direction
                         if direction_name == "destination":
                             process_and_stock_dict[resource + " at " + direction_name]["current stock"] = firm_selected.to_stock_dict[resource]
                         else:
                             process_and_stock_dict[resource + " at " + direction_name]["current stock"] = firm_selected.from_stock_dict[resource]
                         process_and_stock_dict[resource + " at " + direction_name]["rate"] = "NA"
                 
            else:
                process_and_stock_dict = {}
                for direction in ["input","output"]:
                    for resource in firm_selected.input_output_dict[direction]:
                         process_and_stock_dict[resource] = {}
                         process_and_stock_dict[resource]["direction"] = direction
                         process_and_stock_dict[resource]["current stock"] = firm_selected.stock_dict[resource]
                         process_and_stock_dict[resource]["rate"] = firm_selected.input_output_dict[direction][resource]
        
            self.fast_list = gui_components.fast_list(self.action_surface, process_and_stock_dict, rect = self.rect,column_order = ["rownames","direction","rate","current stock"])
        
            














class construct_base_menu():
    """
    The functions in which new bases can be build
    """
    def __init__(self,solar_system_object,action_surface):
        self.solar_system_object_link = solar_system_object
        self.rect = pygame.Rect(150,150,300,300)
        self.action_surface = action_surface
        self.text_receiver = None




    def receive_click(self,event):
        if self.ok_button.rect.collidepoint(event.pos) == 1:
            return self.ok_button.activate(None)

        if self.cancel_button.rect.collidepoint(event.pos) == 1:
            return self.cancel_button.activate(None)



    def exit(self, label, function_parameter):
        return "clear"
        
            
    def new_base_ask_for_name(self,sphere_coordinates, give_length_warning = False):
        """
        Function that prompts the user for a name of the new base
        Optional argument give_length_warning includes a label that specifies max " + str(global_variables.max_letters_in_company_names) + " characters
        """
        
        pygame.draw.rect(self.action_surface, (212,212,212), self.rect)
        pygame.draw.rect(self.action_surface, (0,0,0), self.rect, 2)
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0] + self.rect[2], self.rect[1]))
        pygame.draw.line(self.action_surface, (255,255,255), (self.rect[0], self.rect[1]), (self.rect[0], self.rect[1] + self.rect[3]))

        description = global_variables.standard_font.render("Enter name for base at (" + str(round(sphere_coordinates[0]))+ "," + str(round(sphere_coordinates[1])) + "):",True,(0,0,0))
        self.action_surface.blit(description, (self.rect[0] + self.rect[2]/2 - 100, self.rect[1] + self.rect[3] / 2 - 70))
        if give_length_warning:
            warning = global_variables.standard_font.render("Name must be unique",True,(0,0,0))
            self.action_surface.blit(warning, (self.rect[0] + self.rect[2]/2 - 100, self.rect[1] + self.rect[3] / 2 - 30))
            
            
        self.text_receiver = gui_components.entry(self.action_surface, 
                             topleft = (self.rect[0] + self.rect[2]/2 - 100, self.rect[1] + self.rect[3] / 2), 
                             width = 200, 
                             max_letters = global_variables.max_letters_in_company_names)
        self.text_receiver.active = True

        self.ok_button = gui_components.button("ok", 
                                                self.action_surface,
                                                self.new_base_build, function_parameter = sphere_coordinates, 
                                                fixed_size = (100,35), 
                                                topleft = (self.rect[0] + self.rect[2] - 110, self.rect[1] + self.rect[3] - 40))
        
        self.cancel_button = gui_components.button("cancel", 
                                                self.action_surface,
                                                self.exit, function_parameter = None, 
                                                fixed_size = (100,35), 
                                                topleft = (self.rect[0] + self.rect[2] - 220, self.rect[1] + self.rect[3] - 40))

    def new_base_build(self,label,sphere_coordinates):
        name = self.text_receiver.text
        
        
        #test if name is unique
        unique = True
        for planet_instance in self.solar_system_object_link.planets.values():
            if name in planet_instance.bases.keys():
                unique = False
        
        if 0 < len(name) <= global_variables.max_letters_in_company_names and unique:
            
#            (self,base_name,home_planet,base_data,owner,manager)
            home_planet = self.solar_system_object_link.current_planet
            building_base = self.solar_system_object_link.current_planet.current_base
            base_data = {
                         "northern_loc":sphere_coordinates[1],
                         "eastern_loc":sphere_coordinates[0],
                         "population":100,
                         "country":self.solar_system_object_link.current_player.name,
                         "GDP_per_capita_in_dollars":building_base.gdp_per_capita_in_dollars
                         }
            owner = self.solar_system_object_link.current_player
            
            new_base = company.base(self.solar_system_object_link,name,home_planet,base_data,owner)
            owner.home_cities[name] = new_base
            
            #making the trade route from the founding base
            distance = home_planet.calculate_distance(sphere_coordinates, building_base.position_coordinate)
            transport_type = "ground transport"
            endpoints = [new_base.base_name,building_base.base_name] #try to remove this if you get the opportunity FIXME
            endpoint_links = [new_base,building_base]
            trade_route = {"distance":distance[0],"transport_type":transport_type,"endpoints":endpoints,"endpoint_links":endpoint_links} #converting distance from list to float (has to be list see planet
            new_base.trade_routes[building_base.base_name] = trade_route
            building_base.trade_routes[new_base.base_name] = trade_route
            
            home_planet.bases[name] = new_base
            
            owner.owned_firms[name] = new_base


            print_dict = {"text":"Building a base named " + str(name) + " at " + str(sphere_coordinates),"type":"general gameplay info"}
            self.solar_system_object_link.messages.append(print_dict)

            #clear up everything to make space
            self.solar_system_object_link.display_mode = "planetary"
            return "clear"
            
        else:
            print_dict = {"text":"the selected name " + str(name) + " was too long. Has to be less than " + str(global_variables.max_letters_in_company_names) + " characters","type":"general gameplay info"}
            self.solar_system_object_link.messages.append(print_dict)

            self.new_base_ask_for_name(sphere_coordinates,give_length_warning=True)

