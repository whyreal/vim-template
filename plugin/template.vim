command! -range Tset call template#SetTemplate(<line1>, <line2>)
command! -range Trender call template#RenderTemplate(<line1>, <line2>)
command! Tunset call template#UnSetTemplate()
