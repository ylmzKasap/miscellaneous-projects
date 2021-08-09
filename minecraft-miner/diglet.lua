local robot = require("robot")
local computer = require("computer")
local component = require("component")
local ic = component.proxy(component.list("inventory_controller")())
local nav = component.proxy(component.list("navigation")())
local sides = require("sides")

BLOCKS_TOGO = 4
INV_SIZE = math.floor(robot.inventorySize())
MAX_ENERGY = math.floor(computer.maxEnergy())

function dumpGarbage()
  trash = {}
  trash["minecraft:cobblestone"] = true
  trash["minecraft:stone"] = true
  trash["minecraft:gravel"] = true
  trash["minecraft:dirt"] = true  
  trash["minecraft:redstone"] = true
  trash["minecraft:torch"] = true
  trash["minecraft:rotten_flesh"] = true
  trash["Tin Ore"] = true
  trash["Copper Ore"] = true
  trash["Silver Ore"] = true    
  trash["Cinnabar Ore"] = true

  for i = 1,INV_SIZE do
    robot.select(i)
    itemInfo = ic.getStackInInternalSlot(i)
    if itemInfo ~= nill then
      if trash[itemInfo.name] == true then
        robot.drop()
      elseif trash[itemInfo.label] == true then
        robot.drop()
        end
      end
    end
  end

function GPS(rightLeft, frontBack)
  local facing = nav.getFacing()
  if facing == sides["front"] then
    frontBack = frontBack + 1
  elseif facing == sides["back"] then
    frontBack = frontBack - 1
  elseif facing == sides["right"] then
    rightLeft = rightLeft + 1
  else
    rightLeft = rightLeft - 1
    end
  return rightLeft, frontBack    
  end

function emptyInventory()
  for i = 1,INV_SIZE do
    robot.select(i)
    robot.drop()
    end
  end

function recharge()
  while computer.energy() < (MAX_ENERGY / 100) * 99 do
    os.sleep(3)
    end
  end

function goBack(rightLeft, frontBack)
  robot.turnLeft()
  robot.turnLeft()
  rightLeft, frontBack = moveHorizontal(rightLeft, frontBack)
  robot.turnLeft()
  robot.turnLeft()
  return rightLeft, frontBack
  end

function moveHorizontal(rightLeft, frontBack)
  block, phase = robot.detect()
  while block == true do
    robot.swing()
    block, phase = robot.detect()
    end
  rightLeft, frontBack = GPS(rightLeft, frontBack)
  robot.forward()
  return rightLeft, frontBack
  end

function moveUp(upDown)
  block, phase = robot.detectUp()
  while block == true do
    robot.swingUp()
    block, phase = robot.detectUp()
    end
  upDown = upDown + 1
  robot.up()
  return upDown
  end

function moveDown(upDown)
  block, phase = robot.detectDown()
  while block == true do
    robot.swingDown()
    block, phase = robot.detectDown()
    end
  upDown = upDown - 1
  robot.down()
  return upDown
  end  
        
function goToEpisode(episode, rightLeft, upDown, frontBack)
  upDown = moveUp(upDown)  
  for i = 1,(BLOCKS_TOGO * episode) do
    rightLeft, frontBack = moveHorizontal(rightLeft, frontBack)
    end
  return rightLeft, upDown, frontBack
  end

function startDigging(rightLeft, upDown, frontBack)
  robot.turnLeft()
  for i = 1,(BLOCKS_TOGO * 5) do
    rightLeft, frontBack = moveHorizontal(rightLeft, frontBack)
    end
  robot.turnRight()
  dumpGarbage()
  for i = 1,BLOCKS_TOGO do
    for i = 1,BLOCKS_TOGO do
      rightLeft, frontBack = moveHorizontal(rightLeft, frontBack)
      end
    robot.turnRight()
    for i = 1,3 do
      rightLeft, frontBack = moveHorizontal(rightLeft, frontBack)
      end
    robot.turnRight()
    dumpGarbage()
    for i = 1,BLOCKS_TOGO do
      rightLeft, frontBack = moveHorizontal(rightLeft, frontBack)
      end
    robot.turnLeft()
    for i = 1,3 do
      rightLeft, frontBack = moveHorizontal(rightLeft, frontBack)
      end
    robot.turnLeft()
    dumpGarbage()
    end
  return rightLeft, upDown, frontBack
  end

function goHome(rl, ud, fb)
  initialRL = math.abs(rl)
  while rl ~= 0 do
    rl, fb = moveHorizontal(rl, fb)
    newDistance = math.abs(rl)
    if newDistance >= initialRL then
      rl, fb = goBack(rl, fb)
      robot.turnLeft()
      end
    end
  initialFB = math.abs(fb)
  while fb ~= 0 do
    rl, fb = moveHorizontal(rl, fb)
    newDistance = math.abs(fb)
    if newDistance >= initialFB then
      rl, fb = goBack(rl,fb)
      robot.turnLeft()
      end
    end
  dumpGarbage()
  while ud > 0 do
    ud = moveDown(ud)
    end
  while ud < 0 do
    ud = moveUp(ud)
    end    
  end

function beginAgain()
  episode = 1
  for i = 1,20 do
    rl, ud, fb = 0, 0, 0
    rl, ud, fb = goToEpisode(episode, rl, ud, fb)
    rl, ud, fb = startDigging(rl, ud, fb)
    goHome(rl, ud, fb)
    emptyInventory()
    recharge()
    robot.turnRight()
    episode = episode + 1
    end
  end

beginAgain()