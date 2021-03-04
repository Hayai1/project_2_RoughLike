import json,pygame
with open('data/game/gameMap.json') as f:
  data = json.load(f)


screenRect = pygame.Rect(0, 0, 640, 360)
tilesets = ((data["levels"][0])["layerInstances"][0])["gridTiles"]
tile_map = []
for tile in tilesets:
    location = tile["px"]
    imgType = tile["t"]
    tile_map.append([location,imgType])



tile_map = sorted(tile_map , key=lambda k: [k[0][1]])
largesty = tile_map[len(tile_map)-1][0][1]
tile_map = sorted(tile_map , key=lambda k: [k[0][0]])
largestx = tile_map[len(tile_map)-1][0][0]
largestCord = [largestx,largesty]

chunks = {}
chunkTileStartPos= [0,0]
chunkTileEndPos= [8,8]
res = [largestx,largesty]
res = [int((res[0] / 128) + (res[0] % 128 > 0)),int((res[1] / 128) + (res[1] % 128 > 0))]

chunkAmount = int(res[0] * res[1])

for chunk in range(1,chunkAmount+1):
  chunks[chunk] = []

chunk_rects = []
x= 0
y = 0
chunkCounter = 1
for ychunk in range(1,res[1]+1):
  y += 128
  for xchunk in range(1,res[0]+1):
    chunk_rects.append([chunkCounter,pygame.Rect(x, y, 128, 128)])
    x+=128



def chunkmaking(res,counter,tile,chunks,tile_map):
  y = 0
  for ychunk in range(1,res[1]+1):
    y += 128  
    for xchunk in range(1,res[0]+1):
      #check if tile falls into this chunk
      largestxy = [xchunk * 128, y]
      smallestxy = [largestxy[0]-128, largestxy[1]-128]
      tilexy = [tile[0][0],tile[0][1]]
      if tilexy[0] <= largestxy[0] and tilexy[0] >= smallestxy[0]:

        if tilexy[1] <= largestxy[1] and tilexy[1] >= smallestxy[1]:
          #if it's true find out which chunk to asign them too
          #eqution is x + (y * largestxchunk) -largestxchunk -1 (-1 for index) 
          chunk = (int(xchunk) + (int(ychunk) * int(res[0])) - int(res[0]))
          chunks[chunk].append(tile)
          return chunks,tile_map
  counter += 1
counter = 0
for tile in tile_map:
  chunks,tile_map = chunkmaking(res,counter,tile,chunks,tile_map)

tiles = chunks[1]


