public class Solver {
    
    Game game = new ColorGame();
    Spot [] empties = game.getEmpties();        
    int [] possibleValues = game.getPossibles(); 
    Spot [] [] matrix = game.getMatrix();
    String fileName = "color.txt";

    public Solver(Game g, String fn){
	this.game = g;
	this.fileName=fn;
	this.empties = game.getEmpties();
	this.possibleValues = game.getPossibles();
	this.matrix = game.getMatrix();
    }
    
    public void fillSpots(){
	game.addFile(fileName);
	game.fillSpots();
    }
    
    public boolean label (int iAmLabelling){
	if (iAmLabelling==empties.length){
	    return game.constraintsWork(empties[iAmLabelling-1]);
	}
	
	for (int v = 0; v<possibleValues.length; v++){
	    
	    empties[iAmLabelling].setValue(possibleValues[v]);
	    
	    if(game.constraintsWork(empties[iAmLabelling])){
			if (label(iAmLabelling+1)){
			    return true;}
	    }
	    
	}
	empties[iAmLabelling].setValue(0);
	return false;
	
    }

    def label (curr):
	if curr==len(students):
 	    return constraints_work(students[curr-1])
	student = students[curr]
 	for clubIX in range(0, len(clubs)):
 	    if constraints_work(student, clubs[clubIX]):
 	    	student.put_in(clubIX)
 			if (label(curr+1)):
 			    return true
	    
 	student.remove_from_club()
 	return false
  
    
}